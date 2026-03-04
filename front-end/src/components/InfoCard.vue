<script setup>
	import { defineProps, computed } from 'vue';
	import { toPersianNumbers } from '@/utils/toPersianNumbers.js';

	const props = defineProps({
		id: Number,
		image: String,
		title: String,
		time: String,
		summary: String,
		categories: Array,
	});

	const imageSrc = computed(() => {
		return `/blogs/blog${props.id}/${props.image}`;
	});
</script>

<template>
	<router-link :to="{ name: 'Blog', query: { blogNumber: props.id } }">
		<div class="blog-card">
			<img class="blog-card__image" :src="imageSrc" :alt="title" />
			<h4 class="blog-card__title">{{ title }}</h4>
			<div class="blog-card__details">
				<h5>زمان مطالعه: {{ toPersianNumbers(time) }} دقیقه</h5>
				<div class="blog-card__categories">
					<h5>دسته بندی:</h5>
					<h6
						v-for="category in categories"
						:key="category"
						class="blog-card__category"
					>
						{{ category }}
					</h6>
				</div>
			</div>
			<h5 class="blog-card__summary">{{ summary }}</h5>
		</div>
	</router-link>
</template>

<style lang="scss" scoped>
	.blog-card {
		background-color: var(--primary-600);
		border: space(1) solid var(--primary-100);
		border-radius: space(6);
		width: space(100);
		padding: space(10);
		@include flexbox(column, center, right, space(2));

		&__image {
			width: space(100);
			height: space(100);
			object-fit: cover;
			border-radius: space(4);
		}

		&__title {
			color: var(--text-700);
			height: space(32);
			@include lineClamp(2);
		}

		&__details {
			padding-right: space(4);
			border-right: space(1) solid var(--text-900);
			color: var(--text-300);
			@include flexbox(column, center, right, space(4));
		}

		&__categories {
			height: space(12);
			overflow: hidden;
			@include flexbox(row, start, start, space(2));
		}

		&__category {
			color: var(--text-900);
			background-color: var(--secondary-100);
			padding: space(0) space(4);
			border-radius: space(4);
		}

		&__summary {
			height: space(42);
			color: var(--text-500);
			@include lineClamp();
		}
	}

	.blog-card:hover {
		border: space(1) solid transparent;
		box-shadow: space(0) space(0) space(5) space(3) var(--primary-100);
	}
</style>
