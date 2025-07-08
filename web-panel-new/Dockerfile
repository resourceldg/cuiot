# Dockerfile para desarrollo de SvelteKit
FROM node:20-alpine

# Crear directorio de trabajo
WORKDIR /app

# Copiar package.json y lockfile
COPY package.json package-lock.json* pnpm-lock.yaml* yarn.lock* ./

# Instalar dependencias
RUN npm install

# Copiar el resto del código
COPY . .

# Exponer el puerto de desarrollo
EXPOSE 5173

# Comando por defecto: modo desarrollo
CMD ["npm", "run", "dev", "--", "--host"] 