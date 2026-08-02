<script setup>
	import { toPersianDigits } from '@/utils/toPersianDigits';
	import { addCommas } from '@/utils/addCommas';

	const props = defineProps({
		doctor: {
			type: Object,
			required: true,
		},
	});
</script>

<template>
	<div class="doctor-info">
		<TheTitle label="اطلاعات پزشک" />
		<div class="doctor-info__container">
			<section class="doctor-info__header">
				<img src="/doctor1.png" class="doctor-info__avatar" />
				<h2 class="doctor-info__name">دکتر {{ doctor?.name }}</h2>
			</section>
			<section class="doctor-info__row">
				<div class="doctor-info__item item">
					<span class="item__label">تخصص:</span>
					<h3 class="item__value">{{ doctor?.field }}</h3>
				</div>
				<div class="doctor-info__item item">
					<span class="item__label">میانگین امتیازات دریافتی:</span>
					<h3 v-if="doctor?.score !== 0" class="item__value">
						{{
							toPersianDigits(
								`${doctor?.score} (${doctor?.comments?.length} امتیاز)`,
							)
						}}
					</h3>
					<h3 v-else class="item__value">بدون امتیاز</h3>
				</div>
			</section>
			<section class="doctor-info__row">
				<div class="doctor-info__item item">
					<span class="item__label">قیمت ویزیت (ساعت):</span>
					<h3 class="item__value">{{ addCommas(doctor?.price) }}</h3>
				</div>
				<div class="doctor-info__item item">
					<span class="item__label">سابقه کار:</span>
					<h3 class="item__value">
						{{ toPersianDigits(doctor?.experience || 0) }} سال
					</h3>
				</div>
			</section>
			<section class="doctor-info__row">
				<div class="doctor-info__item item">
					<span class="item__label">موقعیت مطب:</span>
					<h3 class="item__value">{{ doctor?.location }}</h3>
				</div>
				<div class="doctor-info__item item">
					<span class="item__label">ساعت کاری:</span>
					<h3 class="item__value">
						از {{ toPersianDigits(doctor?.start_working_hour) }} تا
						{{ toPersianDigits(doctor?.end_working_hour) }}
					</h3>
				</div>
			</section>
		</div>
	</div>
</template>

<style lang="scss" scoped>
	.doctor-info {
		width: 100%;
		@include flexbox(column, center, start, space(10), nowrap);

		&__container {
			width: 100%;
			background-color: var(--bg-800);
			box-sizing: border-box;
			padding: space(6);
			border-radius: space(10);
			@include flexbox(row, center, center, space(6));

			@media (max-width: $md) {
				@include flexbox(column, center, start, space(6));
			}
		}

		&__header {
			width: 100%;
			padding-bottom: space(6);
			border-bottom: space(0.5) solid var(--text-500);
			@include flexbox(row, center, center, space(6), nowrap);

			@media (max-width: $md) {
				@include flexbox(column, center, center, space(6));
			}
		}

		&__avatar {
			width: space(50);
			height: space(50);
			object-fit: cover;
			border-radius: 50%;
		}

		&__name {
			color: var(--title-500);
			flex: 1;
		}

		&__row {
			width: 100%;
			@include flexbox(row, center, start, space(0), nowrap);

			@media (max-width: $md) {
				@include flexbox(column, center, start, space(0));
			}
		}

		.item {
			width: 100%;
			@include flexbox(row, start, center, space(2), nowrap);

			&__label {
				font-size: space(10);
				color: var(--text-600);
				@include lineClamp(1);

				@media (max-width: $md) {
					font-size: space(8);
				}
			}

			&__value {
				color: var(--text-800);
				@include lineClamp(1);

				@media (max-width: $md) {
					font-size: space(8);
				}
			}
		}
	}
</style>
