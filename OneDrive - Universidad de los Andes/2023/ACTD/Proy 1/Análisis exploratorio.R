options(scipen = 999)
library(dplyr)
library(ggplot2) 
library(readxl)
library(gmodels)
library(Hmisc)
library(ggthemes)
library(dplyr)

#Recuerden cambiar el directorio de trabajo
datos=Data
colnames(datos)=c("age", "sex", "cp", "trestbps","chol","fbs","restecg","thalach","exang","oldpeak","slope","ca","thal","Diagnostico")
datos=subset(datos, ca !="?")
datos=subset(datos, thal !="?")



head(datos)

glimpse(datos)

datos$ca=as.numeric(datos$ca)
datos$thal=as.numeric(datos$thal)

glimpse(datos)

### pasamos a factor el disgnóstico?

### variables categoricas
table(datos$exang)
table(datos$slope)
table(datos$thal)
table(datos$Diagnostico)


table(datos$Diagnostico,datos$exang)
table(datos$Diagnostico,datos$exang, datos$slope)


##si quisieramos verlo como proporciones
prop.table(table(datos$Diagnostico,datos$exang))

#¿cómo hacemos si queremos ver porcentajes por fila o columna?.Esto lo hacemos poniendo una coma y luego 1 (filas) o 2 (columnas).
prop.table(table(datos$Diagnostico,datos$exang),1)


###podemos poner únicamente una variable y nos muestra de una vez las proporciones
CrossTable(datos$Diagnostico)



###varibles discretas
summary(datos)
describe(datos)



##histogramas

hist(datos$thalach)
hist(datos$age, breaks = 4)######## 4 clases.
summary(hist(datos$age, breaks = 4))

hist(datos$trestbps) ### discretizar por categoria


hist(datos$oldpeak)
hist(datos$ca)

#Cargar paquetes
library(GGally)
library(corrplot)
library(PerformanceAnalytics)

##grafico de correlación
correlacion<-round(cor(datos), 1)

corrplot(correlacion, method="number", type="upper")