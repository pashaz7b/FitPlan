# مرحله build
FROM node:18-alpine AS builder

WORKDIR /app

# نصب پکیج‌ها
COPY package*.json ./
RUN npm install

# کپی بقیه فایل‌ها
COPY . .

# ساخت خروجی production با Vite
RUN npm run build

# مرحله دوم: Nginx برای ارائه frontend
FROM nginx:stable-alpine

# حذف فایل‌های پیش‌فرض nginx
RUN rm -rf /usr/share/nginx/html/*

# کپی خروجی build به nginx
COPY --from=builder /app/dist /usr/share/nginx/html

# کانفیگ nginx برای پشتیبانی از React Router
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
