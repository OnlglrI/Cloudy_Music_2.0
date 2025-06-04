для prod режима
NODE_ENV=production docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build

для dev
docker compose up
