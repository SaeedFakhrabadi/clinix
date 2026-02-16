<script setup>
	import { computed, onMounted, ref } from 'vue';
	import { useRouter } from 'vue-router';
	import { useToast } from 'vue-toastification';
	import { doctorsList } from '@/services/doctors';
	import { addCommas } from '@/utils/addCommas';

	const router = useRouter();
	const toast = useToast();

	const doctors = ref([]);

	const searchQuery = ref('');
	const sortQuery = ref('none');

	const fieldFilter = ref('all');
	const locationFilter = ref('all');
	const scoreFilter = ref('all');

	const loading = ref(false);
	const tableHeaders = [
		{ label: 'نام پزشک', value: 'name' },
		{ label: 'تخصص', value: 'field' },
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

	const fieldOptions = computed(() => {
		const set = new Set(doctors.value.map((d) => d.field));
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
					d.field.toLowerCase().includes(sq),
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
		if (fieldFilter.value !== 'all') {
			list = list.filter((d) => d.field === fieldFilter.value);
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
			query: { did: row.id },
		});
	};

	onMounted(async () => {
		loading.value = true;
		try {
			const response = await doctorsList();
			doctors.value = response.data;
		} catch (error) {
			console.error('Error : ', error?.response?.data || error?.message);
			toast.error(error?.response?.data?.message ?? 'خطا در برقراری ارتباط');
			doctors.value = [];
		} finally {
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
					v-model="fieldFilter"
					:options="fieldOptions"
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
			:headers="tableHeaders"
			:rows="mappedDoctors"
			:loading="loading"
			@row-click="handleRowClick"
		/>
	</section>
</template>

<style lang="scss" scoped>
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
