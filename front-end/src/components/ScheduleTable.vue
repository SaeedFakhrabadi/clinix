<script setup>
	import { computed, ref } from 'vue';
	import { useRouter } from 'vue-router';
	import { useToast } from 'vue-toastification';
	import { addCommas } from '@/utils/addCommas';
	import { toPersianDigits } from '@/utils/toPersianDigits';
	import { toEnglishDigits } from '@/utils/toEnglishDigits';

	const props = defineProps({
		doctor: {
			type: Object,
			required: true,
		},
		currentUser: {
			type: Object,
			required: true,
		},
	});

	const emit = defineEmits(['pay']);

	const router = useRouter();
	const toast = useToast();

	const weekOffset = ref(0);

	const reserveModalText = ref('');
	const payModalText = ref('');
	const isReserveModalOpen = ref(false);
	const isPayModalOpen = ref(false);

	const reservationData = ref({});
	const transactionData = ref({});

	const payMethod = ref('BANK');

	const WEEK_DAYS = [
		'شنبه',
		'یکشنبه',
		'دوشنبه',
		'سه‌شنبه',
		'چهارشنبه',
		'پنجشنبه',
	];
	const DAYS_IN_WEEK = 6;
	const SCHEDULE_HOURS = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21];

	const getIranDayAndHour = () => {
		const d = new Date();
		const jsDay = d.getDay();
		const iranDay = (jsDay + 1) % 7;
		const hour = d.getHours();
		return { dayIndex: iranDay, hour };
	};

	const getScheduleCellClass = (cellValue) => {
		if (cellValue === 'قابل رزرو') return 'cell--reservable';
		if (cellValue === 'رزرو شده') return 'cell--reserved';
		return '';
	};

	const gregorianToJalali = (gy, gm, gd) => {
		const g_d_m = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334];
		let jy = gy <= 1600 ? 0 : 979;
		gy -= gy <= 1600 ? 621 : 1600;
		const gy2 = gm > 2 ? gy + 1 : gy;
		let days =
			365 * gy +
			Math.floor((gy2 + 3) / 4) -
			Math.floor((gy2 + 99) / 100) +
			Math.floor((gy2 + 399) / 400) -
			80 +
			gd +
			g_d_m[gm - 1];
		jy += 33 * Math.floor(days / 12053);
		days %= 12053;
		jy += 4 * Math.floor(days / 1461);
		days %= 1461;
		jy += Math.floor((days - 1) / 365);
		if (days > 365) days = (days - 1) % 365;
		const jm =
			days < 186
				? 1 + Math.floor(days / 31)
				: 7 + Math.floor((days - 186) / 30);
		const jd = 1 + (days < 186 ? days % 31 : (days - 186) % 30);
		return { year: jy, month: jm, day: jd };
	};

	const scheduleGrid = computed(() => {
		const {
			start_working_hour,
			end_working_hour,
			reserved_times = {},
		} = props.doctor;

		const { dayIndex: todayDayIndex, hour: todayHour } = getIranDayAndHour();
		const isCurrentWeek = weekOffset.value === 0;

		const weekStartDayIndex = weekOffset.value * DAYS_IN_WEEK;

		return SCHEDULE_HOURS.map((hour) => {
			const inWorkingHours =
				hour >= start_working_hour && hour < end_working_hour;
			const cells = [];

			for (let dayOffset = 0; dayOffset < DAYS_IN_WEEK; dayOffset++) {
				const absoluteDay = weekStartDayIndex + dayOffset;

				const isPast =
					isCurrentWeek &&
					(absoluteDay < todayDayIndex + 1 ||
						(absoluteDay === todayDayIndex + 1 && hour <= todayHour));

				if (isPast) {
					cells.push({ dayIndex: dayOffset, status: 'past' });
					continue;
				}

				const reservedHours = reserved_times[absoluteDay] || [];
				const reserved = reservedHours.includes(hour);

				let status = 'unavailable';
				if (inWorkingHours) status = reserved ? 'reserved' : 'free';

				cells.push({ dayIndex: dayOffset, status });
			}

			return { hour, cells };
		});
	});

	const weekDayDates = computed(() => {
		const now = new Date();
		const jsDay = now.getDay();
		const iranDay = (jsDay + 1) % 7;
		const saturdayOffset = iranDay;

		const thisSaturday = new Date(now);
		thisSaturday.setDate(now.getDate() - saturdayOffset);

		const start = new Date(thisSaturday);
		start.setDate(thisSaturday.getDate() + weekOffset.value * 7);

		const dates = [];
		for (let i = 0; i < DAYS_IN_WEEK; i++) {
			const d = new Date(start);
			d.setDate(start.getDate() + i);
			const j = gregorianToJalali(
				d.getFullYear(),
				d.getMonth() + 1,
				d.getDate(),
			);
			dates.push(
				`${j.year}/${String(j.month).padStart(2, '0')}/${String(j.day).padStart(2, '0')}`,
			);
		}
		return dates;
	});

	const scheduleTableHeaders = computed(() => [
		{ label: 'ساعت', value: 'hour' },
		...WEEK_DAYS.map((dayName, i) => ({
			label: `${dayName} ${weekDayDates.value[i]}`,
			value: `day${i}`,
		})),
	]);

	const scheduleTableRows = computed(() => {
		if (!scheduleGrid.value.length) return [];

		return scheduleGrid.value.map((row) => {
			const r = {
				hour: `${row.hour} تا ${row.hour + 1}`,
			};
			row.cells.forEach((cell, dayIndex) => {
				r[`day${dayIndex}`] =
					cell.status === 'free'
						? 'قابل رزرو'
						: cell.status === 'reserved'
							? 'رزرو شده'
							: '-';
			});
			return r;
		});
	});

	const scheduleWeekLabel = computed(() =>
		weekOffset.value === 0 ? 'هفته جاری' : 'هفته آینده',
	);

	const setCurrentWeek = () => (weekOffset.value = 0);
	const setNextWeek = () => (weekOffset.value = 1);

	const pay = () => {
		isPayModalOpen.value = false;

		transactionData.value = {
			method: payMethod.value,
			pid: props.currentUser?.id,
			price: props.doctor?.price,
			type: 'PAY',
		};

		emit('pay', { reservationData, transactionData });
	};

	const reserve = () => {
		isReserveModalOpen.value = false;
		payModalText.value = 'روش پرداخت خود را انتخاب کنید';
		isPayModalOpen.value = true;
	};

	const timeFormatter = (date, firstCellValue) => {
		const persianDate = date.split(' ');
		const englishDate = toEnglishDigits(persianDate[1]);
		const formattedDate = englishDate.replaceAll('/', '-');
		const formattedHour = firstCellValue.split('تا');
		return `${formattedDate}-${formattedHour[0].trim()}`;
	};

	const handleCellClick = (cell) => {
		const { cellValue, firstCellValue, header } = cell;

		if (cellValue === firstCellValue) {
			return;
		}

		if (!props.currentUser) {
			router.push({ name: 'Login' });
			toast.error('!برای رزرو نوبت ابتدا وارد حساب کاربری خود شوید');
			return;
		}

		if (props.currentUser?.role?.value === 'DOCTOR') {
			toast.error('!امکان رزرو نوبت برای پزشکان وجود ندارد');
			return;
		}

		if (cellValue === '-') {
			toast.error('!زمان انتخاب شده قابل رزرو نمی باشد');
			return;
		}

		if (cellValue === 'رزرو شده') {
			toast.error('!زمان انتخاب شده قبلاً رزرو شده است');
			return;
		}

		reservationData.value = {
			did: props.doctor.did,
			pid: props.currentUser.id,
			time: timeFormatter(header.label, firstCellValue),
		};

		reserveModalText.value = `
			آیا می خواهید نوبت ساعت ${toPersianDigits(firstCellValue)}
		 	در تاریخ ${toPersianDigits(header?.label)}
		  را با دکتر ${props.doctor?.name}
			به مبلغ ${addCommas(props.doctor?.price)}
			رزرو کنید؟`;
		isReserveModalOpen.value = true;
	};
</script>

<template>
	<div class="schedule-table">
		<TheTitle label="برنامه زمانی" has-divider/>
		<div class="schedule-table__week-nav">
			<TheButton
				type="hollow"
				label="نمایش هفته جاری"
				:is-disabled="weekOffset === 0"
				@click="setCurrentWeek"
			/>
			<span class="schedule-table__label">
				برنامه زمانی {{ scheduleWeekLabel }}
			</span>
			<TheButton
				type="hollow"
				label="نمایش هفته آینده"
				:is-disabled="weekOffset === 1"
				@click="setNextWeek"
			/>
		</div>
		<div class="schedule-table__table">
			<TheTable
				clickMode="cell"
				:headers="scheduleTableHeaders"
				:rows="scheduleTableRows"
				:get-cell-class="getScheduleCellClass"
				@cell-click="handleCellClick"
			/>
		</div>
		<TheModal
			v-if="isReserveModalOpen"
			:text="reserveModalText"
			submit-label="رزرو"
			@close="isReserveModalOpen = false"
			@submit="reserve"
		/>
		<TheModal
			v-if="isPayModalOpen"
			:text="payModalText"
			submit-label="پرداخت"
			@close="isPayModalOpen = false"
			@submit="pay"
		>
			<template v-slot:content>
				<h4 class="schedule-table__text">
					مبلغ پرداختی : {{ addCommas(doctor.price) }}
				</h4>
				<TheSelect
					label="روش پرداخت"
					icon-name="pay"
					v-model="payMethod"
					:options="[
						{ label: 'درگاه بانکی', value: 'BANK' },
						{ label: 'کیف پول', value: 'WALLET' },
					]"
				/>
			</template>
		</TheModal>
	</div>
</template>

<style lang="scss" scoped>
	.schedule-table {
		width: 100%;
		@include flexbox(column, center, start, space(10));

		&__week-nav {
			width: 100%;
			@include flexbox(row, space-between, center, space(5), nowrap);
		}

		&__label {
			width: 100%;
			color: var(--text-900);
			text-align: center;

			@media (max-width: $sm) {
				display: none;
			}
		}

		&__table {
			width: 100%;

			:deep(.cell--reservable) {
				color: var(--success-100);
			}

			:deep(.cell--reserved) {
				color: var(--danger-100);
			}
		}

		&__text {
			color: var(--text-900);
		}
	}
</style>
