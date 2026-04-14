# .

This template should help get you started developing with Vue 3 in Vite.

## Recommended IDE Setup

[VS Code](https://code.visualstudio.com/) + [Vue (Official)](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

## Recommended Browser Setup

- Chromium-based browsers (Chrome, Edge, Brave, etc.):
  - [Vue.js devtools](https://chromewebstore.google.com/detail/vuejs-devtools/nhdogjmejiglipccpnnnanhbledajbpd)
  - [Turn on Custom Object Formatter in Chrome DevTools](http://bit.ly/object-formatters)
- Firefox:
  - [Vue.js devtools](https://addons.mozilla.org/en-US/firefox/addon/vue-js-devtools/)
  - [Turn on Custom Object Formatter in Firefox DevTools](https://fxdx.dev/firefox-devtools-custom-object-formatters/)

## Customize configuration

See [Vite Configuration Reference](https://vite.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Compile and Minify for Production

```sh
npm run build
```

### Lint with [ESLint](https://eslint.org/)

```sh
npm run lint
```


## 1. Serverda backup olish
``` 
docker exec -t mira-db pg_dump -U mira_user mira_db > mira_dump_$(date +%Y-%m-%d).sql

```

## 2. Localda recovery qilish
```
# 1. Eski bazani o'chirish va ochish (xatoliklar bo'lmasligi uchun)
docker exec -it mira-db psql -U mira_user -d postgres -c "DROP DATABASE mira_db;"
docker exec -it mira-db psql -U mira_user -d postgres -c "CREATE DATABASE mira_db;"

# 2. Ma'lumotlarni tiklash
cat mira_dump.dump | docker exec -i mira-db pg_restore -U mira_user -d mira_db -v --no-owner --no-privileges

```
