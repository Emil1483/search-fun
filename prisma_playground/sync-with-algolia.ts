import { PrismaClient, Product, ProductImage, ProductMetadata } from '@prisma/client'
import algoliasearch from 'algoliasearch';
import { SingleBar, Presets } from 'cli-progress'
import { inflateRawSync } from 'zlib';

const prisma = new PrismaClient()

const client = algoliasearch(process.env.ALGOLIA_APP_ID!, process.env.ALGOLIA_API_KEY!);
const index = client.initIndex('products');

async function* getProducts() {
    let lastProductId: string | undefined
    const take = 5000

    while (true) {
        const products = await prisma.product.findMany({
            take: take,
            skip: lastProductId ? 1 : 0,
            ...lastProductId
                ? { cursor: { id: lastProductId } }
                : {},
            where: {
                id: { not: '' }
            },
            orderBy: [
                { createdAt: 'desc' },
                { id: 'asc' },
            ],
            include: {
                metadata: true,
                images: true,
            },
        })

        if (products.length == 0) break

        lastProductId = products[products.length - 1].id

        yield* products

        if (products.length < take) break
    }
}

async function syncWithAlgolia() {
    await index.clearObjects()

    const count = await prisma.product.count({
        where: {
            id: { not: '' }
        },
    })

    const algoliaObjects = []

    const loadingBar = new SingleBar({}, Presets.shades_classic)
    loadingBar.start(count, 0)

    for await (const product of getProducts()) {
        const algoliaObject: any = product

        if (algoliaObject.images) {
            algoliaObject.images = [algoliaObject.images[0]]
        }

        algoliaObject.objectID = algoliaObject.id
        delete algoliaObject.id

        algoliaObjects.push(algoliaObject)
        loadingBar.update(algoliaObjects.length)
    }

    loadingBar.stop()

    await index.saveObjects(algoliaObjects).catch((e) => {
        console.warn(e)
    })
}

syncWithAlgolia()