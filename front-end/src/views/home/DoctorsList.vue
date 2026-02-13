<script setup>
	import { computed, onMounted, ref } from 'vue';
	import { useRouter } from 'vue-router';
	import { doctorsList } from '@/services/doctors';
	import { addCommas } from '@/utils/addCommas';

	const router = useRouter();

	const doctors = ref([]);

	const searchQuery = ref('');
	const sortQuery = ref('none');

	const specialtyFilter = ref('all');
	const locationFilter = ref('all');
	const scoreFilter = ref('all');

	const loading = ref(false);
	const headers = [
		{ label: 'نام پزشک', value: 'name' },
		{ label: 'تخصص', value: 'specialty' },
		{ label: 'موقعیت', value: 'location' },
		{ label: 'هزینه (به ازای هر ساعت)', value: 'price' },
		{ label: 'امتیاز از 5', value: 'score' },
	];

	const sortOptions = [
		{ value: 'score-desc', label: 'بیشترین امتیاز' },
		{ value: 'score-asc', label: 'کمترین امتیاز' },
		{ value: 'price-desc', label: 'گران ترین' },
		{ value: 'price-asc', label: 'ارزان ترین' },
	];

	const specialtyOptions = computed(() => {
		const set = new Set(doctors.value.map((d) => d.specialty));
		return [
			{ value: 'all', label: 'همه تخصص ها' },
			...Array.from(set).map((value) => ({ value, label: value })),
		];
	});

	const locationOptions = computed(() => {
		const set = new Set(doctors.value.map((d) => d.location));
		return [
			{ value: 'all', label: 'همه موقعیت ها' },
			...Array.from(set).map((value) => ({ value, label: value })),
		];
	});

	const scoreOptions = computed(() => {
		const set = new Set(doctors.value.map((d) => d.score));
		const scores = Array.from(set).sort((a, b) => a - b);
		return [
			{ value: 'all', label: 'همه امتیاز ها' },
			...scores.map((value) => ({
				value: String(value),
				label: value,
			})),
		];
	});

	const searchDoctors = (list) => {
		const sq = searchQuery.value.trim().toLowerCase();
		if (sq) {
			list = list.filter(
				(d) =>
					d.name.toLowerCase().includes(sq) ||
					d.specialty.toLowerCase().includes(sq),
			);
		}

		return list;
	};

	const sortDoctors = (list) => {
		list.sort((a, b) => {
			switch (sortQuery.value) {
				case 'score-asc':
					return Number(a.score) - Number(b.score);
				case 'score-desc':
					return Number(b.score) - Number(a.score);
				case 'price-asc':
					return Number(a.price) - Number(b.price);
				case 'price-desc':
					return Number(b.price) - Number(a.price);
				default:
					return 0;
			}
		});

		return list;
	};

	const filterBySpecialty = (list) => {
		if (specialtyFilter.value !== 'all') {
			list = list.filter((d) => d.specialty === specialtyFilter.value);
		}

		return list;
	};

	const filterByLocation = (list) => {
		if (locationFilter.value !== 'all') {
			list = list.filter((d) => d.location === locationFilter.value);
		}

		return list;
	};

	const filterByScore = (list) => {
		if (scoreFilter.value !== 'all') {
			const score = Number(scoreFilter.value);
			list = list.filter((d) => Number(d.score) === score);
		}

		return list;
	};

	const mappedDoctors = computed(() => {
		let list = [...doctors.value];
		const searchedDoctors = searchDoctors(list);
		const filteredBySpecialty = filterBySpecialty(searchedDoctors);
		const filteredByLocationty = filterByLocation(filteredBySpecialty);
		const filteredByScore = filterByScore(filteredByLocationty);
		const sortedDoctors = sortDoctors(filteredByScore);

		return sortedDoctors.map((doctor) => ({
			...doctor,
			price: addCommas(doctor.price),
		}));
	});

	const handleRowClick = ({ row }) => {
		router.push({
			name: 'DoctorDetails',
			query: { id: row.id },
		});
	};

	onMounted(async () => {
		loading.value = true;
		try {
			const response = await doctorsList();
			console.log('🚀 ~ response:', response.data);
		} catch (error) {
			console.error('Failed to fetch doctors list:', error);
		} finally {
			doctors.value = [
				{
					id: 1,
					name: 'دکتر علی رضایی',
					specialty: 'قلب و عروق',
					location: 'تهران',
					price: 200_000,
					score: 5,
				},
				{
					id: 2,
					name: 'دکتر نسرین احمدی',
					specialty: 'مغز و اعصاب',
					location: 'اصفهان',
					price: 300_000,
					score: 4,
				},
				{
					id: 3,
					name: 'دکتر سارا کریمی',
					specialty: 'پوست و مو',
					location: 'شیراز',
					price: 250_000,
					score: 5,
				},
				{
					id: 4,
					name: 'دکتر مهدی حسینی',
					specialty: 'اطفال',
					location: 'تبریز',
					price: 180_000,
					score: 3,
				},
			];
			loading.value = false;
		}
	});
</script>

<template>
	<section class="doctors-list">
		<h2 class="doctors-list__title">لیست پزشکان کلینیک</h2>
		<div class="doctors-list__controls">
			<div class="doctors-list__search-sort">
				<TheInput
					v-model="searchQuery"
					label="جستجوی پزشک بر اساس نام یا تخصص"
					icon-name="search"
					placeholder="نام یا تخصص پزشک را وارد کنید"
				/>
				<TheSelect
					v-model="sortQuery"
					:options="sortOptions"
					icon-name="sort"
					label="مرتب سازی بر اساس"
				/>
			</div>
			<div class="doctors-list__filters">
				<TheSelect
					v-model="specialtyFilter"
					:options="specialtyOptions"
					label="فیلتر بر اساس تخصص"
					icon-name="filter"
				/>
				<TheSelect
					v-model="locationFilter"
					:options="locationOptions"
					label="فیلتر بر اساس موقعیت"
					icon-name="filter"
				/>
				<TheSelect
					v-model="scoreFilter"
					:options="scoreOptions"
					label="فیلتر بر اساس امتیاز"
					icon-name="filter"
				/>
			</div>
		</div>
		<h4 class="doctors-list__text">
			برای مشاهده جزییات مربوط به پزشک و رزرو نوبت ، روی پزشک مورد نظر کلیک
			کنید:
		</h4>
		<TheTable
			:headers="headers"
			:rows="mappedDoctors"
			:loading="loading"
			@row-click="handleRowClick"
		/>
	</section>
</template>

<style scoped lang="scss">
	.doctors-list {
		padding-left: space(6);
		width: 100%;
		@include flexbox(column, center, start, space(14), nowrap);

		&__title {
			color: var(--text-900);
			padding-right: space(4);
			border-right: space(4) solid var(--title-100);
		}

		&__controls {
			width: 100%;
			@include flexbox(column, center, start, space(0), nowrap);
		}

		&__search-sort {
			width: 100%;
			@include flexbox(row, center, center, space(10), nowrap);

			@media (max-width: $sm) {
				@include flexbox(column, center, center, space(0), nowrap);
			}
		}

		&__filters {
			width: 100%;
			@include flexbox(row, center, center, space(10), nowrap);

			@media (max-width: $sm) {
				@include flexbox(column, center, center, space(0), nowrap);
			}
		}

		&__text {
			color: var(--text-900);
		}
	}
</style>
