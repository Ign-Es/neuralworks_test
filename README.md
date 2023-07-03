# Challenge AI Engineer Neuralworks
## Requisitos y respuestas
### 1. ¿Cómo se distribuyen los datos? ¿Qué te llama la atención o cuál es tu conclusión sobreesto?

Debo preguntar ¿Qué datos?¿Todas las columnas dadas en el CSV?. Las columnas contienen datos de distinto tipo, y pueden ser representadas de diferentes maneras para visualizar su distribución. Si bien es posible crear todas estas visualizaciones y examinar su distribución, esto no resulta ser útil para cumplir el objetivo de este desafío.


El desafío es un problema de clasificación probabilística en el cual se busca la probabilidad de que el vuelo sea clasificado como atrasado o no. En cuanto a los datos se busca en primer lugar lidiar con aquellos datos nulos, en este caso solo hay un dato nulo en la columna Vlo-O, fila 6068, el cual no afecta para responder requisitos posteriores, ni el entrenamiento del modelo. También se busca medir el balance del dataset que puede influir en el rendimiento de los modelos. El dataset es imbalanceado, con una razón cercana a 2:1 entre atraso y no atraso. El imbalance es menor y por ende no afectará de manera significativa el rendimiento de los modelos al ser entrenados con este dataset. Luego en el proceso de feature selection se elegirá cual de estos datos es relevante para obtener la probabilidad de atraso del vuelo.


### 2. Genera las columnas adicionales y luego expórtelas en un archivo synthetic_features.csv.

Se incluye el archivo "synthetic_features.csv" en el repositorio. Una consideración, cuando se menciona "valor entre x e y", se considera como x <= valor <= y. 

### 3. Entrena uno o varios modelos usando los algoritmos que prefieras para estimar la probabilidad de atraso de un vuelo. Siéntete libre de generar variables adicionales y/o  complementar con variables externas.

El desafío se trata de un problema de clasificacion probabilistica, y por ende se probaran modelos que comunmente obtienen buenos resultados en estos problemas, como:  Logistic Regression, Gaussian Process Classifier, Decission Trees, Support Vector Machines y Gradient Boosted Machines.

En cuanto a features que son utilizadas para predecir la probabilidad de atraso, se eliminan todas aquellas que contienen informacion acerca del vuelo en operacion.

### 4. Escoge el modelo que a tu criterio tenga una mejor performance, argumentando tu decisión.
El modelo se selecciona en base a su 'accuracy' obtenida al momento de predecir si el vuelo se atrasa o no, en un subconjunto de datos pruebas.


### 5. Serializa el mejor modelo seleccionado e implementa una API REST para poder predecir atrasos de nuevos vuelos.
Modelo serializado y guardado en carpeta 'models' con nombre 'best_model.pkl'

### 6. Automatiza el proceso de build y deploy de la API, utilizando uno o varios servicios cloud. Argumenta tu decisión sobre los servicios utilizados.

### 7. Realiza pruebas de estrés a la API con el modelo expuesto con al menos 50.000 requests durante 45 segundos. Para esto debes utilizar esta herramienta y presentar las métricas obtenidas. ¿Cómo podrías mejorar la performance de las pruebas anteriores?