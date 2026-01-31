import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import path from 'path';
import Components from 'unplugin-vue-components/vite';
import svgLoader from 'vite-svg-loader';

export default defineConfig({
	resolve: {
		alias: {
			'@': path.resolve(__dirname, './src'),
		},
	},
	plugins: [
		vue(),
		svgLoader(),
		Components({
			dirs: ['src'],
			extensions: ['vue'],
			deep: true,
			dts: './components.d.ts',
		}),
	],
	css: {
		preprocessorOptions: {
			scss: {
				additionalData: `
          @use "@/assets/styles/abstracts/functions" as *;
          @use "@/assets/styles/abstracts/colors" as *;
          @use "@/assets/styles/abstracts/mixins" as *;
          @use "@/assets/styles/abstracts/variables" as *;

          @use "@/assets/styles/base/theme-variables" as *;
          @use "@/assets/styles/base/fonts" as *;
          @use "@/assets/styles/base/typography" as *;
          `,
			},
		},
	},
});
