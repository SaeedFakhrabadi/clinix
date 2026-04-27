<script setup>
	import { toPersianDigits } from '@/utils/toPersianDigits';
	import { addCommas } from '@/utils/addCommas';

	const props = defineProps({
		id: { type: Number, required: true },
		image: { type: String, default: '/Boog.png' },
		name: { type: String, required: true },
		field: { type: String, required: true },
		location: { type: String, required: true },
		price: { type: Number, required: true },
		score: { type: Number, required: true },
	});

	const emits = defineEmits(['select']);

	const handleClick = (id) => emits('select', { id });
</script>

<template>
	<div class="doctor-card" @click="handleClick(id)">
		<div class="doctor-card__header">
			<img class="doctor-card__image" :src="image" :alt="name" />
			<h3 class="doctor-card__name">دکتر {{ name }}</h3>
		</div>
		<div class="doctor-card__section">
			<h4 class="doctor-card__item">
				<TheIcon name="id-card" class="doctor-card__icon" />
				{{ field }}
			</h4>
			<h4 class="doctor-card__item">
				<TheIcon name="fill-star" class="doctor-card__star-icon" />
				{{ toPersianDigits(score !== 0 ? score : 'بدون امتیاز') }}
			</h4>
		</div>
		<div class="doctor-card__section">
			<h4 class="doctor-card__item">
				<TheIcon name="sort" class="doctor-card__icon" />
				{{ location }}
			</h4>
			<h4 class="doctor-card__item">{{ addCommas(price) }}</h4>
		</div>
	</div>
</template>

<style lang="scss" scoped>
	.doctor-card {
		background-color: var(--primary-900);
		box-shadow: space(0) space(0) space(6) var(--text-100);
		border-radius: space(10);
		cursor: pointer;
		width: calc(25% - space(21));
		padding: space(6);
		transition: all 0.4s ease;
		@include flexbox(column, center, right, space(2));

		@media (max-width: $lg) {
			width: calc(33% - space(19));
		}

		@media (max-width: $md) {
			width: calc(50% - space(18));
		}

		@media (max-width: $sm) {
			width: calc(100% - space(0));
		}

		&:hover {
			background-color: var(--primary-600);
			box-shadow: space(0) space(0) space(6) var(--text-900);
		}

		&__header {
			width: 100%;
			padding-bottom: space(6);
			border-bottom: space(0.5) solid var(--text-100);
			@include flexbox(row, center, center, space(6));
		}

		&__image {
			width: 40%;
			height: space(72);
			object-fit: cover;
			border-radius: space(4);
		}

		&__name {
			flex: 1;
			color: var(--title-500);
			height: space(72);
			@include lineClamp(3);
		}

		&__section {
			width: 100%;
			color: var(--text-700);
			@include flexbox(row, space-between, center, space(6));
		}

		&__item {
			@include flexbox(row, center, center, space(2));
		}

		&__icon {
			color: var(--text-100);
		}

		&__star-icon {
			color: var(--warning-100);
		}
	}
</style>
