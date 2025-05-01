

import numpy as np
# data = np.load('/home/paperspace/Documents/nika_space/main_dataset/ade/images/ADE_train_00000600.npy', allow_pickle=True)
data = np.load('/home/paperspace/Documents/nika_space/dataset_later/train_raw_challenge_npy/100.npy', allow_pickle=True)

print("Type:", type(data))
print("Shape:", getattr(data, 'shape', 'No shape'))
print("Dtype:", getattr(data, 'dtype', 'No dtype'))


if isinstance(data, np.ndarray):
    print("Preview:")
    print(data)

    if np.issubdtype(data.dtype, np.number):
        print("Min:", np.min(data))
        print("Max:", np.max(data))
    else:
        print("Array is not numeric, skipping min/max.")
        

elif isinstance(data, (dict, list, tuple)):
    print("Content:")
    print(data)
else:
    print("Unsupported data type.")
