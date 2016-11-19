import pymongo as mongo
import matplotlib.pyplot as plt

from convnet import ConvNetVGG

def get_db():
    # Start a MongoClient with default settings (lookup localhost)
    client = mongo.MongoClient()

    # Connect to the Northwind database
    db = client.Yelp

    return db

def display_business(name, stars, predictions, raw_im):
    predictions_sorted = sorted([(prediction, count) for prediction, count in predictions.iteritems()],
                                key=lambda (k, v): -v)
    # Display information
    plt.figure()
    plt.imshow(raw_im.astype('uint8'))
    plt.axis('off')
    plt.text(250, 10, "%s (ratings: %.1f stars)" % (name, stars))

    for n, (prediction, count) in enumerate(predictions_sorted):
        plt.text(250, 70 + n * 20, '{}. {} ({})'.format(n + 1, prediction, count), fontsize=12)
    plt.show()


def get_businesses_predictions(size):
    db = get_db()

    businesses = db.business.aggregate([
        {
            # Sample 5 randoms documents
            "$sample": {
                "size": size
            }
        },
        # Project the information that is interesting
        {
            "$project": {
                "name": "$name",
                "business_id": "$business_id",
                "stars": "$stars",
                # To not display the id
                "_id": 0
            }
        }
    ])

    vgg = ConvNetVGG()

    for business in businesses:
        rand_business_id = business["business_id"]
        photos_for_business = db.photo.find({ "business_id": rand_business_id})
        photos_for_business = [1,2,3,4]
        predictions_business = {}
        last_raw_im = None
        for photo in photos_for_business:
            # TODO Get photo path from photo
            photo_path = "yelp_dataset/o.jpg"
            current_predictions, raw_im = vgg.process_image(photo_path, return_raw_img=True)

            # Collect all the predictions in a map to get their importance
            for prediction in current_predictions:
                if prediction not in predictions_business:
                    predictions_business[prediction] = 0
                predictions_business[prediction] += 1

            last_raw_im = raw_im
        print predictions_business
        display_business(business["name"], business["stars"], predictions_business, last_raw_im)


if "__main__" == __name__:
    get_businesses_predictions(1)





