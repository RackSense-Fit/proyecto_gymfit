# vendor/
Esta carpeta contiene bibliotecas JS y pesos de modelos de visión servidos en /static/vendor/.
NO colocar aquí imágenes de ejercicios (usar /exercise-images/).

## Inventario de Archivos Locales

| Archivo | Tamaño | Procedencia | Versión | Licencia |
|---|---|---|---|---|
| `tf.min.js` | 1,469,843 bytes (~1.47 MB) | npm `@tensorflow/tfjs` (vía CDN jsDelivr) | 4.22.0 | Apache-2.0 |
| `coco-ssd.min.js` | 9,299 bytes (~9.3 KB) | npm `@tensorflow-models/coco-ssd` (vía CDN jsDelivr) | 2.2.3 | Apache-2.0 |
| `model.json` | 527,315 bytes (~527 KB) | Google Cloud Storage (`storage.googleapis.com/tfjs-models/savedmodel/ssdlite_mobilenet_v2/model.json`) | no verificado (modelo SSDLite MobileNet V2) | Apache-2.0 |
| `group1-shard1of5` | 4,194,304 bytes (4.00 MB) | Google Cloud Storage (`storage.googleapis.com/tfjs-models/savedmodel/ssdlite_mobilenet_v2/group1-shard1of5`) | no verificado | Apache-2.0 |
| `group1-shard2of5` | 4,194,304 bytes (4.00 MB) | Google Cloud Storage (`storage.googleapis.com/tfjs-models/savedmodel/ssdlite_mobilenet_v2/group1-shard2of5`) | no verificado | Apache-2.0 |
| `group1-shard3of5` | 4,194,304 bytes (4.00 MB) | Google Cloud Storage (`storage.googleapis.com/tfjs-models/savedmodel/ssdlite_mobilenet_v2/group1-shard3of5`) | no verificado | Apache-2.0 |
| `group1-shard4of5` | 4,194,304 bytes (4.00 MB) | Google Cloud Storage (`storage.googleapis.com/tfjs-models/savedmodel/ssdlite_mobilenet_v2/group1-shard4of5`) | no verificado | Apache-2.0 |
| `group1-shard5of5` | 1,257,312 bytes (1.20 MB) | Google Cloud Storage (`storage.googleapis.com/tfjs-models/savedmodel/ssdlite_mobilenet_v2/group1-shard5of5`) | no verificado | Apache-2.0 |

## Fecha de Descarga

- **Fecha:** 15 y 16 de octubre de 2026 (incorporado formalmente en el repositorio en el commit `6976f54` del 9 de noviembre de 2026).

## Procedimiento para Volver a Descargarlos

Para volver a descargar los archivos desde sus repositorios oficiales hacia `src/api/static/vendor/`:

### En Linux / macOS / Git Bash (curl):
```bash
cd src/api/static/vendor

# TensorFlow.js v4.22.0
curl -fLo tf.min.js https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@4.22.0/dist/tf.min.js

# COCO-SSD v2.2.3
curl -fLo coco-ssd.min.js https://cdn.jsdelivr.net/npm/@tensorflow-models/coco-ssd@2.2.3/dist/coco-ssd.min.js

# Manifiesto y grafo del modelo (SSDLite MobileNet V2)
curl -fLo model.json https://storage.googleapis.com/tfjs-models/savedmodel/ssdlite_mobilenet_v2/model.json

# Shards de pesos binarios (shards 1 a 5)
for i in 1 2 3 4 5; do
  curl -fLo group1-shard${i}of5 https://storage.googleapis.com/tfjs-models/savedmodel/ssdlite_mobilenet_v2/group1-shard${i}of5
done
```

### En Windows PowerShell:
```powershell
Set-Location src/api/static/vendor

Invoke-WebRequest -Uri "https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@4.22.0/dist/tf.min.js" -OutFile "tf.min.js"
Invoke-WebRequest -Uri "https://cdn.jsdelivr.net/npm/@tensorflow-models/coco-ssd@2.2.3/dist/coco-ssd.min.js" -OutFile "coco-ssd.min.js"
Invoke-WebRequest -Uri "https://storage.googleapis.com/tfjs-models/savedmodel/ssdlite_mobilenet_v2/model.json" -OutFile "model.json"

1..5 | ForEach-Object {
    Invoke-WebRequest -Uri "https://storage.googleapis.com/tfjs-models/savedmodel/ssdlite_mobilenet_v2/group1-shard$($_)of5" -OutFile "group1-shard$($_)of5"
}
```

