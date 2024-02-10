gcloud builds submit --tag gcr.io/apprevexus/Catalogue-scoring-app  --project=apprevexus

gcloud run deploy --image gcr.io/apprevexus/Catalogue-scoring-app --platform managed  --project=apprevexus --allow-unauthenticated