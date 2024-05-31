#============================================================
# PROGRAMA DE RECONOCIMIENTO DE USAURIOS AUTORIZADOS
# Autor: David Barreto Lara
#===========================================================
#%% 1. LIBRERÍAS
from deepface import DeepFace
from datetime import datetime

import cv2, os


#%% 2. VARIABLES GLOBALES
detector_backends = ['opencv', 'retinaface','mtcnn', 'ssd', 'dlib', 'mediapipe', 'yolov8', 'centerface','skip']
models = ['VGG-Face', 'Facenet', 'Facenet512', 'OpenFace', 'DeepFace', 'DeepID', 'Dlib', 'ArcFace', 'SFace', 'GhostFaceNet']
distances=['cosine', 'euclidean', 'euclidean_l2']

DET_BACK = detector_backends[1]
MODEL = models[1]
DISTANCE = distances[1]

db_dir = 'my_db'
target_dir = 'my_ref_db'
tmp_dir='tmp'

user_dict={'user001':'Scarlet',
           'user002':'Will',
           'user003':'Leonardo',
           'user004':'Gal',
           'user005':'Daniel',
           'user006':'Elijah',
           'user007':'David'}

#%% 3. FUNCIONES
def IdentifyFace(imgPath, dbPath):
    try:
        #Identificando persona
        dfs = DeepFace.find(img_path=imgPath,
                            db_path=dbPath, 
                            model_name=MODEL, 
                            detector_backend=DET_BACK, 
                            distance_metric=DISTANCE)
    except Exception as e:
        print(f"Ocurrió un error al intentar identificar la cara: {e}")
        return None    
    
    # Resultados de la verificación de rostros
    ComparisonOutput= dfs[0]

    # Si el dataframe está vacío, devolver "Usuario no autorizado"
    if ComparisonOutput.empty:
        return "Usuario no autorizado"

    # Ubicando el registro con menor valor de distance
    idx = ComparisonOutput['distance'].idxmin()

    # Obteniendo el "user" correspondiente
    userPath = ComparisonOutput.loc[idx, 'identity']

    # Encontrando el nombre correspondiente
    tag = userPath.split('\\')[1]
    return user_dict[tag]
    

def captura_imagen(cam):
    # Verifica si la carpeta 'tmp' existe y la crea si no
    if not os.path.exists('tmp'):
        os.makedirs('tmp')
    
    # Crea una ventana de visualización
    cv2.namedWindow("Captura de imagen")

    print(f"Mire fijamente a la cámara y sonria...")

    # Muestra la imagen de la cámara en la ventana hasta que se presione la tecla 's'
    while True:
        ret, frame = cam.read()
        if not ret:
            print("No se pudo leer un frame de la cámara. Por favor, verifica que tu cámara esté funcionando correctamente.")
            return None, None
        cv2.imshow("Captura de imagen", frame)

        now = datetime.now()
        timestamp = now.strftime("%Y%m%d_%H%M%S")

        # Si se presiona la tecla 's', se guarda la imagen y se sale del bucle
        if cv2.waitKey(1) & 0xFF == ord('s'):
            img_path = f'tmp/capture_{timestamp}.jpg'
            cv2.imwrite(img_path, frame)
            print("Captura tomada exitosamente.....")
            break

    # Cierra la ventana de visualización
    cv2.destroyAllWindows()

    # Devuelve la ruta de la imagen guardada
    return img_path, frame

#%% PROGRAMA PRINCIPAL
if __name__ == "__main__":
    # Inicializa la cámara
    cam = cv2.VideoCapture(0)

    while True:
        try:
            # Captura las imágenes
            my_image, frame = captura_imagen(cam)
            
            FaceUser = IdentifyFace(my_image, db_dir)
            #print(FaceUser)

            print("###############################################")
            if FaceUser=='Usuario no autorizado':
                print("Usted no esta autorizado")
            else:
                print(f"\t\tBienvenido {FaceUser}")
            print("###############################################")

            # Pregunta al usuario si desea realizar otro reconocimiento
            respuesta = input("¿Desea realizar otro reconocimiento? (s/n): ")
            if respuesta.lower() != 's':
                break

        except Exception as e:
            print(f"Ocurrió un error: {e}")
            break

    # Cierra la cámara
    cam.release()
