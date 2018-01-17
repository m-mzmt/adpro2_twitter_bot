import learning_cat_keras as learn
import numpy as np



def classifier(np_img):
    img_array = []
    img_array.append(np.asarray(np_img))
    img_array = np.array(img_array)

    model = learn.build_model(img_array.shape[1:])
    model.load_weights("cat.hdf5")


    predict = model.predict(img_array)


    print(predict)

    return predict






