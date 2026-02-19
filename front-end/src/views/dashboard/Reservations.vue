<script setup>
	import { onMounted, ref, computed } from 'vue';
	import { useToast } from 'vue-toastification';
	import { storeToRefs } from 'pinia';
	import { getReservations, deleteReservation } from '@/services/reservations';
	import { createTransaction } from '@/services/transactions';
	import { useCurrentUserStore } from '@/stores/currentUser';
	import { toPersianDigits } from '@/utils/toPersianDigits';
	import jalaali from 'jalaali-js';

	const toast = useToast();

	const reservations = ref(null);
	const loading = ref(true);
	const error = ref(null);

	const currentUserStore = useCurrentUserStore();
	const { currentUser } = storeToRefs(currentUserStore);

	const reservationId = ref(0);

	const modalText = ref('');
	const isModalOpen = ref(false);

	const tableHeaders = [
		{ label: 'نام پزشک', value: 'doctor_name' },
		{ label: 'تاریخ نوبت', value: 'date' },
		{ label: 'ساعت', value: 'hour' },
		{ label: 'وضعیت', value: 'is_active' },
	];

	const removeReservation = async () => {
		isModalOpen.value = false;
		try {
			deleteReservation(reservationId.value);
			
			createTransaction('BANK', currentUser.value?.id, 300_000, 'REFUND');

			reservations.value = reservations.value.filter(
				(item) => item.id !== reservationId.value,
			);
		} catch (error) {
			console.error('Error : ', error?.response?.data || error?.message);

			toast.error(error?.response?.data?.message ?? 'خطا در برقراری ارتباط');
		}
	};

	const handleRowClick = ({ row }) => {
		if (row.is_active !== 'فعال') {
			toast.error('!نوبت انتخاب شده منقضی شده است و نمی توان آن را لغو کرد');
			return;
		}

		reservationId.value = row.id;

		modalText.value = `
	     آیا از لغو نوبت دکتر ${row.doctor_name}
	     در تاریخ ${toPersianDigits(row.date)}
	     ساعت  ${toPersianDigits(row.hour)}
	     اطمینان دارید؟`;
		isModalOpen.value = true;
	};

	const mappedReservations = computed(() => {
		if (!reservations.value) return [];

		return reservations.value.map((reservation) => {
			const dateObj = new Date(reservation.start_reservation_time);
			const { jy, jm, jd } = jalaali.toJalaali(
				dateObj.getUTCFullYear(),
				dateObj.getUTCMonth() + 1,
				dateObj.getUTCDate(),
			);

			const persianDate = `${jy}/${String(jm).padStart(2, '0')}/${String(jd).padStart(2, '0')}`;

			const hour = dateObj.getUTCHours();

			return {
				id: reservation.id,
				doctor_name: reservation.doctor_name,
				is_active: reservation.is_past ? 'منقضی' : 'فعال',
				date: persianDate,
				hour: `${hour} تا ${hour + 1}`,
			};
		});
	});

	onMounted(async () => {
		loading.value = true;
		try {
			const response = await getReservations(currentUser.value?.id);
			reservations.value = response?.data?.reservations;
		} catch (error) {
			console.error('Error : ', error?.response?.data || error?.message);

			toast.error(error?.response?.data?.message ?? 'خطا در برقراری ارتباط');

			reservations.value = [];
		} finally {
			loading.value = false;
		}
	});
</script>

<template>
	<div class="reservations">
		<div v-if="loading" class="reservations__state--loading">
			<h2>در حال دریافت اطلاعات نوبت ها...</h2>
		</div>
		<div v-else-if="error" class="reservations__state--error">
			<h2>خطا در دریافت اطلاعات نوبت ها!</h2>
		</div>
		<div v-else-if="reservations?.length" class="reservations__container">
			<h2 class="reservations__title">لیست نوبت ها</h2>
			<p class="reservations__text">
				برای لغو نوبت روی سطر نوبت مورد نظر در جدول کلیک کنید
			</p>
			<TheTable
				:headers="tableHeaders"
				:rows="mappedReservations"
				:loading="loading"
				@row-click="handleRowClick"
			/>
			<TheModal
				v-if="isModalOpen"
				:text="modalText"
				submit-label="لغو نوبت"
				@close="isModalOpen = false"
				@submit="removeReservation"
			/>
		</div>
	</div>
</template>

<style lang="scss" scoped>
	.reservations {
		padding-left: space(6);
		width: 100%;
		@include flexbox(column, center, center, space(14), nowrap);

		&__state {
			&--loading {
				color: var(--text-500);
			}
			&--error {
				color: var(--danger-500);
			}
		}

		&__container {
			width: 100%;
			@include flexbox(column, center, start, space(14), nowrap);
		}

		&__title {
			color: var(--text-900);
			padding-right: space(4);
			border-right: space(4) solid var(--title-100);
		}

		&__text {
			color: var(--text-700);
		}
	}
</style>
