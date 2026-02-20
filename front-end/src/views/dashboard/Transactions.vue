<script setup>
	import { onMounted, ref, computed } from 'vue';
	import { useRouter } from 'vue-router';
	import { useToast } from 'vue-toastification';
	import { storeToRefs } from 'pinia';
	import { useCurrentUserStore } from '@/stores/currentUser';
	import { toPersianDigits } from '@/utils/toPersianDigits';
	import { addCommas } from '@/utils/addCommas';
	import { getTransactions } from '@/services/transactions';
	import jalaali from 'jalaali-js';

	const router = useRouter();
	const toast = useToast();

	const transactions = ref(null);
	const loading = ref(true);
	const loadingError = ref(null);

	const currentUserStore = useCurrentUserStore();
	const { currentUser } = storeToRefs(currentUserStore);

	const transactionData = ref(0);

	const modalText = ref('');
	const isModalOpen = ref(false);

	const tableHeaders = [
		{ label: 'تاریخ', value: 'date' },
		{ label: 'ساعت', value: 'hour' },
		{ label: 'قیمت', value: 'price' },
		{ label: 'نوع تراکنش', value: 'type' },
		{ label: 'روش تراکنش', value: 'method' },
		{ label: 'وضعیت', value: 'status' },
	];

	const downloadFactor = () => {
		isModalOpen.value = false;

		const factorContent = `
		<!DOCTYPE html>
		<html dir="rtl" lang="fa">
		<head>
			<meta charset="UTF-8">
			<style>
      *{font-family: 'yekan-regular', sans-serif; }
				body { font-family: Arial, sans-serif; }
				.factor { max-width: 300px; margin: 0 auto; padding: 20px; }
				.factor__title { color: #333; text-align: center; }
				.factor__item { display: flex; justify-content: space-between; margin: 30px 0; }
				.factor__label { color: #666;  margin: 0px;}
				.factor__value { color: #000; font-weight: bold; margin: 0px;}
			</style>
		</head>
		<body>
			<div class="factor">
				<h3 class="factor__title">فاکتور تراکنش</h3>
				<div class="factor__item">
					<span class="factor__label">تاریخ:</span>
					<h4 class="factor__value">${transactionData.value.date}</h4>
				</div>
				<div class="factor__item">
					<span class="factor__label">ساعت:</span>
					<h4 class="factor__value">${transactionData.value.hour}</h4>
				</div>
				<div class="factor__item">
					<span class="factor__label">قیمت:</span>
					<h4 class="factor__value">${transactionData.value.price}</h4>
				</div>
				<div class="factor__item">
					<span class="factor__label">نوع تراکنش:</span>
					<h4 class="factor__value">${transactionData.value.type}</h4>
				</div>
				<div class="factor__item">
					<span class="factor__label">روش تراکنش:</span>
					<h4 class="factor__value">${transactionData.value.method}</h4>
				</div>
				<div class="factor__item">
					<span class="factor__label">وضعیت:</span>
					<h4 class="factor__value">${transactionData.value.status}</h4>
				</div>
			</div>
		</body>
		</html>
	`;

		const blob = new Blob([factorContent], { type: 'text/html' });
		const url = URL.createObjectURL(blob);
		const link = document.createElement('a');
		link.href = url;
		link.download = `factor_${transactionData.value.date.replace(/\//g, '-')}.html`;
		document.body.appendChild(link);
		link.click();
		document.body.removeChild(link);
		URL.revokeObjectURL(url);
	};

	const handleRowClick = ({ row }) => {
		transactionData.value = row;

		modalText.value = '';
		isModalOpen.value = true;
	};

	const mappedTransactions = computed(() => {
		if (!transactions.value) return [];

		return transactions.value.map((transaction) => {
			const dt = new Date(transaction.date);

			const jy = dt.getFullYear();
			const jm = dt.getMonth() + 1;
			const jd = dt.getDate();

			const {
				jy: persianYear,
				jm: persianMonth,
				jd: persianDay,
			} = jalaali.toJalaali(jy, jm, jd);

			const persianDate = `${persianYear}/${String(persianMonth).padStart(2, '0')}/${String(persianDay).padStart(2, '0')}`;

			const hourLocal = dt.getHours();
			const minuteLocal = dt.getMinutes();
			const timeStr = `${String(hourLocal).padStart(2, '0')}:${String(minuteLocal).padStart(2, '0')}`;

			const typeMap = {
				PAY: 'پرداخت وجه',
				REFUND: 'بازگشت وجه',
			};

			const methodMap = {
				WALLET: 'کیف پول',
				BANK: 'حساب بانکی',
			};

			const statusMap = {
				SUCCESS: 'موفق',
				FAILURE: 'نا موفق',
			};

			return {
				price: addCommas(transaction.price),
				type: typeMap[transaction.type] || transaction.type,
				method: methodMap[transaction.method] || transaction.method,
				status: statusMap[transaction.status] || transaction.status,
				date: toPersianDigits(persianDate),
				hour: toPersianDigits(timeStr),
			};
		});
	});

	onMounted(async () => {
		loading.value = true;
		try {
			const response = await getTransactions(currentUser.value?.id);
			transactions.value = response?.data?.transactions;

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
	<div class="transactions">
		<div v-if="loading" class="transactions__state--loading">
			<h2>در حال دریافت اطلاعات تراکنش ها...</h2>
		</div>
		<div v-else-if="loadingError" class="transactions__state--error">
			<h2>خطا در دریافت اطلاعات تراکنش ها!</h2>
		</div>
		<div v-else-if="transactions?.length" class="transactions__container">
			<h2 class="transactions__title">لیست تراکنش ها</h2>
			<p class="transactions__text">
				برای مشاهده و دانلود فاکتور تراکنش روی سطر تراکنش مورد نظر در جدول کلیک
				کنید
			</p>
			<TheTable
				:headers="tableHeaders"
				:rows="mappedTransactions"
				@row-click="handleRowClick"
			/>
			<TheModal
				v-if="isModalOpen"
				:text="modalText"
				submit-label="دانلود فاکتور"
				@close="isModalOpen = false"
				@submit="downloadFactor"
			>
				<template v-slot:content class="transactions__factor factor">
					<h3 class="factor__title">فاکتور تراکنش</h3>
					<div class="factor__item">
						<span class="factor__label">تاریخ:</span>
						<h4 class="factor__value">{{ transactionData.date }}</h4>
					</div>
					<div class="factor__item">
						<span class="factor__label">ساعت:</span>
						<h4 class="factor__value">{{ transactionData.hour }}</h4>
					</div>
					<div class="factor__item">
						<span class="factor__label">قیمت:</span>
						<h4 class="factor__value">{{ transactionData.price }}</h4>
					</div>
					<div class="factor__item">
						<span class="factor__label">نوع تراکنش:</span>
						<h4 class="factor__value">{{ transactionData.type }}</h4>
					</div>
					<div class="factor__item">
						<span class="factor__label">روش تراکنش:</span>
						<h4 class="factor__value">{{ transactionData.method }}</h4>
					</div>
					<div class="factor__item">
						<span class="factor__label">وضعیت:</span>
						<h4 class="factor__value">{{ transactionData.status }}</h4>
					</div>
				</template>
			</TheModal>
		</div>
		<div v-else class="transactions__state--empty">
			<h2>در حال حاضر تراکنشی وجود ندارد!</h2>
		</div>
	</div>
</template>

<style lang="scss" scoped>
	.transactions {
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

		.factor {
			width: 100%;
			@include flexbox(column, center, center, space(14), nowrap);

			&__title {
				color: var(--text-700);
			}

			&__item {
				width: 100%;
				@include flexbox(row, space-between, start, space(14), nowrap);
			}

			&__label {
				color: var(--text-500);
			}

			&__value {
				color: var(--text-900);
			}
		}
	}
</style>
