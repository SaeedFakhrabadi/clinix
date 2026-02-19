<script setup>
	import { onMounted, ref, computed } from 'vue';
	import { useRouter } from 'vue-router';
	import { useToast } from 'vue-toastification';
	import { storeToRefs } from 'pinia';
	import { getReservations, deleteReservation } from '@/services/reservations';
	import { createTransaction } from '@/services/transactions';
	import { useCurrentUserStore } from '@/stores/currentUser';
	import { toPersianDigits } from '@/utils/toPersianDigits';
	import jalaali from 'jalaali-js';

	const router = useRouter();
	const toast = useToast();

	const reservations = ref(null);
	const loading = ref(true);
	const loadingError = ref(null);

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
			if (
				error?.response?.data?.detail ===
				'Authentication credentials were not provided.'
			) {
				toast.error('!زمان ورود شما منقضی شده است، لطفا دوباره وارد شوید');
				currentUserStore.removeCurrentUser();
				router.push({ name: 'Login' });
				return;
			}

			console.error('Error : ', error?.response?.data || error?.message);

			toast.error(error?.response?.data?.message ?? 'خطا در برقراری ارتباط');
		}
	};

	const handleRowClick = ({ row }) => {
		if (row?.is_active !== 'فعال') {
			toast.error('!نوبت انتخاب شده منقضی شده است و نمی توان آن را لغو کرد');
			return;
		}

		reservationId.value = row?.id;

		modalText.value = `
	     آیا از لغو نوبت دکتر ${row?.doctor_name}
	     در تاریخ ${toPersianDigits(row?.date)}
	     ساعت  ${toPersianDigits(row?.hour)}
	     اطمینان دارید؟`;
		isModalOpen.value = true;
	};

	const mappedReservations = computed(() => {
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
				id: reservation?.id,
				// doctor_name: reservation?.doctor_name,
				doctor_name: reservation?.username,
				is_active: reservation?.is_past ? 'منقضی' : 'فعال',
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

			loading.value = false;
		} catch (error) {
			if (
				error?.response?.data?.detail ===
				'Authentication credentials were not provided.'
			) {
				toast.error('!زمان ورود شما منقضی شده است، لطفا دوباره وارد شوید');
				currentUserStore.removeCurrentUser();
				router.push({ name: 'Login' });
				return;
			}

			console.error('Error : ', error?.response?.data || error?.message);

			toast.error(error?.response?.data?.message ?? 'خطا در برقراری ارتباط');

			loading.value = false;
			loadingError.value = true;
		}
	});
</script>

<template>
	<div class="reservations">
		<div v-if="loading" class="reservations__state--loading">
			<h2>در حال دریافت اطلاعات نوبت ها...</h2>
		</div>
		<div v-else-if="loadingError" class="reservations__state--error">
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
		<div v-else class="reservations__state--empty">
			<h2>در حال حاضر نوبتی وجود ندارد!</h2>
		</div>
	</div>
</template>

<style lang="scss" scoped>
	.reservations {
		&__state {
			&--loading {
				color: var(--text-500);
			}
			&--error {
				color: var(--danger-500);
			}
			&--empty {
				color: var(--text-500);
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
