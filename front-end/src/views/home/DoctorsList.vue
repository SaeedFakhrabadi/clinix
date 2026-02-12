<script setup>
	const headers = [
		{ label: 'نام پزشک', value: 'name' },
		{ label: 'تخصص', value: 'specialty' },
		{ label: 'شهر', value: 'city' },
		{ label: 'سال سابقه', value: 'experience' },
	];

	const doctors = [
		{
			id: 1,
			name: 'دکتر علی رضایی',
			specialty: 'قلب و عروق',
			city: 'تهران',
			experience: '12',
		},
		{
			id: 2,
			name: 'دکتر نسرین احمدی',
			specialty: 'مغز و اعصاب',
			city: 'اصفهان',
			experience: '8',
		},
		{
			id: 3,
			name: 'دکتر سارا کریمی',
			specialty: 'پوست و مو',
			city: 'شیراز',
			experience: '10',
		},
		{
			id: 4,
			name: 'دکتر مهدی حسینی',
			specialty: 'اطفال',
			city: 'تبریز',
			experience: 7,
		},
	];
</script>

<template>
	<section class="doctors-list">
		<h3 class="doctors-list__title">لیست پزشکان (ماک دیتا)</h3>

		<TheTable :headers="headers" :rows="doctors" />
	</section>
</template>

<style scoped lang="scss">
	.doctors-list {
		width: 100%;
		@include flexbox(column, flex-start, stretch, space(6), nowrap);

		&__title {
			color: var(--text-900);
		}
	}
</style>
