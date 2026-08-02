FROM node:20-slim AS builder

# ۱. تنظیمات محیطی برای پایداری بیشتر
ENV NODE_OPTIONS="--max-old-space-size=2048"

WORKDIR /app

# ۲. آپدیت npm و تنظیم میرور (یکبار انجام شود بهتر است)
RUN npm install -g npm@latest

#RUN npm config set registry https://mirror-npm.runflare.com && \
#    npm config set strict-ssl false

# ۳. کپی فایل‌های پکیج (برای استفاده از قابلیت Cache لایه‌های داکر)
COPY package*.json ./

RUN rm -f package-lock.json

# ۴. نصب پکیج‌ها با افزایش زمان انتظار برای جلوگیری از Timeout
RUN npm install --verbose --fetch-retries=5 --fetch-retry-mintimeout=20000

# ۵. کپی بقیه کدها و بیلد پروژه
COPY . .
RUN npm run build

# مرحله نهایی: Nginx
FROM nginx:alpine

# کپی فایل‌های ساخته شده از مرحله قبل
# نکته: مطمئن شوید پوشه خروجی شما واقعاً dist است (در برخی پروژه‌ها build است)
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
