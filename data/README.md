In an effort to minimise the image size, no data files are included in this image.
You can however follow the instructions given below to add new data to the project. 
Uncomment "ADD <data_file_name.tar.xz>" and add file name in the Dockerfile if you want to rebuild the
image or add it the usual way using the "docker add" command

	**********************************************************
			INSTRUCTIONS
	**********************************************************

You need to prepare your data in *.mat file with the following format:

    'points': N x 3 array (x, y, z coordinates of the point cloud)
    'labels': N x 1 array (1-based integer per-point labels)
    'category': scalar (0-based integer model category)

