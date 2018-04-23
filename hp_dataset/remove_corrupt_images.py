import os
import tensorflow as tf
from PIL import Image   





for path, subdirs, files in os.walk('./images/'):      
     for file in files:
        extension = file.split('.')[-1]
        if extension == ('jpg' or 'jpeg' or 'JPG' or 'JPEG'):
            fileLoc = os.path.join(path, file)
            img = Image.open(fileLoc)
            if img.mode != 'RGB':
                print(os.path.join(path, file)+" WRONG IMAGE ENCODING")
                print("REMOVING FILE...")
                os.remove(os.path.join(path, file))


filenames = tf.train.match_filenames_once(['./images/*/*.jpg','./images/*/*.JPG','./images/*/*.jpeg','./images/*/*.JPEG'])
count_num_files = tf.size(filenames)
filename_queue = tf.train.string_input_producer(filenames)

reader=tf.WholeFileReader()
key,value=reader.read(filename_queue)
image = tf.image.decode_jpeg(value)

init = tf.global_variables_initializer()
init_l = tf.local_variables_initializer()

with tf.Session() as sess:
    sess.run([init,init_l])
    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(coord=coord)
    num_files = sess.run(count_num_files)
    print("TOTAL NUMBER OF IMAGES: "+num_files.astype(str))
    
    for i in range(num_files):
        try:    
            image_evaled,file_path=sess.run([image,key])
            print(file_path+" IMAGE OK")
        except Exception, e:
            print(file_path+" CORRUPTED IMAGE")
            os.remove(file_path)

    coord.request_stop()
    coord.join(threads)
