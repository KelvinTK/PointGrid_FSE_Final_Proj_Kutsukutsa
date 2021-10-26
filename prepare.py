import numpy as np
import math
import os
from scipy.io import savemat, loadmat
from zipfile import ZipFile
from os.path import basename

FOLDERS_TO_PREPARE = 5  # It will NOT convert full ModelNet40 dataset. Only given number of folders. However,


# network will not change its N_CATEGORIES parameter
# To convert all dataset set = 40


def zipdata(dirName='/content/drive/MyDrive/ModelNetMatFiles'):
    with ZipFile('/content/drive/MyDrive/datasetclear.zip', 'w') as zipObj:
        for folderName, subfolders, filenames in os.walk(dirName):
            for filename in filenames:
                filePath = os.path.join(folderName, filename)
                zipObj.write(filePath, basename(filePath))


def tonumarr(string_arr, filename, VERT):
    numarr = []
    for i, string in enumerate(string_arr):
        if VERT:
            # if filename == "./ModelNet40/bottle/train/bottle_0149.off":
            #  print (string.split(' '))
            a, b, c = string.rstrip().split(' ')
            a, b, c = float(a), float(b), float(c)
        if not VERT:
            n, a, b, c = string.rstrip().split(' ')
            # if filename == "./ModelNet40/bottle/train/bottle_0149.off":
            # print (n)
            # print(a)
            # print(b)
            # print(c)
            a, b, c = int(a), int(b), int(c)
            # print (n,a,b,c)
        numarr.append([a, b, c])
    return np.array(numarr)


def area(a, b, c):
    def distance(p1, p2):
        return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

    side_a = distance(a, b)
    side_b = distance(b, c)
    side_c = distance(c, a)
    s = 0.5 * (side_a + side_b + side_c)
    try:
        area = math.sqrt(s * (s - side_a) * (s - side_b) * (s - side_c))
        return area
    except:
        return ("ERROR")


def randpoint(A, B, C):
    r = np.random.rand(2)
    return (1 - np.sqrt(r[0])) * A + np.sqrt(r[0]) * (1 - r[1]) * B + r[1] * np.sqrt(r[0]) * C


def sample(filename, short_filename):
    print(filename)
    # Read vertices and faces from file
    with open(filename) as ooffile:
        lines = ooffile.readlines()
        if str(lines[0]) != 'OFF\n':
            print('NOT VALID FILE FORMAT')
            return 0
        nVert, nFace, nEdge = lines[1].split(' ')
        nVert, nFace, nEdge = int(nVert), int(nFace), int(nEdge)
        verts = tonumarr(np.array(lines[2:nVert + 2]), filename, True)
        # print(verts)
        faces = tonumarr(np.array(lines[nVert + 2:nVert + nFace + 2]), filename, False)
        # print(faces)
        areas = np.array([area(verts[face[0]], verts[face[1]], verts[face[2]]) for face in faces])
        if "ERROR" in areas:
            print("WRONG FACES DETECTED")
            return 0
        # print(len(verts), len(faces))

    # Sample triangles with probability proportional to treir area
    if True:
        total = areas.sum()
        sample_size = 1024
        choice = np.random.rand(1024) * total
        cum_sum = areas.cumsum()
        cum_array = np.asarray(cum_sum)
        idx = np.searchsorted(cum_array, choice)
        sampled = faces[idx - 1]
    # Compute random points
    randpoints = np.array([randpoint(verts[face[0]], verts[face[1]], verts[face[2]]) for face in sampled])
    # Labels = [1]
    labels = np.zeros_like(randpoints) + 1
    # category
    category = cat_index_dict[short_filename[:-9]]
    category_folder, split_folder, name = filename.split('/')[2:]
    new_filename = '/data/temp/' + str(os.path.join(category_folder, split_folder, name.split(".")[0])) + '.mat'
    # with open(new_filename, 'w') as f:
    #  print ("created")
    if not os.path.exists(os.path.dirname(new_filename)):
        try:
            os.makedirs(os.path.dirname(new_filename))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
    savemat(new_filename, {'points': randpoints, 'labels': labels, 'category': category})
    print("SUCCESS")


cat_list = os.listdir("./ModelNet40")
cat_index_dict = dict(zip(cat_list, range(len(cat_list))))

# Sample
f = []
I = 0
short_filenames = []
for (dirpath, dirnames, filenames) in os.walk("./ModelNet40"):
    if I == FOLDERS_TO_PREPARE + 1:
        break
    fullpath = [os.path.join(dirpath, f) for f in filenames]
    f.append(fullpath)
    short_filenames.append(filenames)
    I += 1
    print(I)
full_filenames = np.concatenate(np.array(f))
short_filenames = np.concatenate(np.array(short_filenames))
for full, short in zip(full_filenames, short_filenames):
    sample(full, short)

# Verify
filelist = []
new_filenames = []
for (dirpath, dirnames, filenames) in os.walk("/data/temp"):
    if dirpath.split('/')[-1] == 'test':
        new_fullpath = ['/data/ShapeNet/test/' + f for f in filenames]
        new_filenames.append(new_fullpath)
    if dirpath.split('/')[-1] == 'train':
        new_fullpath = ['/data/ShapeNet/train/' + f for f in filenames]
        new_filenames.append(new_fullpath)
    fullpath = [os.path.join(dirpath, f) for f in filenames]
    filelist.append(fullpath)

full_filenames = np.concatenate(np.array(filelist))
new_filenames = np.concatenate(np.array(new_filenames))

for new_filename, filename in zip(new_filenames, full_filenames):
    print(filename)
    try:
        mat_content = loadmat(filename)
    except:
        os.remove(filename)
        continue
    pc = mat_content['points']
    labels = np.squeeze(mat_content['labels'])
    category = mat_content['category'][0][0]

    savemat(new_filename, {'points': pc, 'labels': np.zeros(len(pc)) + 1, 'category': category})
