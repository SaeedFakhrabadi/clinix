<script setup>
	import { onMounted, ref, computed } from 'vue';
	import { useToast } from 'vue-toastification';
	import { storeToRefs } from 'pinia';
	import { useCurrentUserStore } from '@/stores/currentUser';
	import { toPersianDigits } from '@/utils/toPersianDigits';
	import { addCommas } from '@/utils/addCommas';
	import { getTransactions } from '@/services/transactions';
	import jalaali from 'jalaali-js';

	const toast = useToast();

	const transactions = ref(null);
	const loading = ref(true);
	const error = ref(null);

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
			const [datePart, timePart] = transaction.date.split(' ');
			const [year, month, day] = datePart.split('-').map(Number);
			const jalaaliDate = jalaali.toJalaali(year, month, day);
			const persianDate = `${jalaaliDate.jy}/${String(jalaaliDate.jm).padStart(2, '0')}/${String(jalaaliDate.jd).padStart(2, '0')}`;

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
				hour: toPersianDigits(timePart.substring(0, 5)),
			};
		});
	});

	onMounted(async () => {
		loading.value = true;
		try {
			const response = await getTransactions(currentUser.value?.id);
			transactions.value = response?.data?.transactions;
		} catch (error) {
			console.error('Error : ', error?.response?.data || error?.message);

			toast.error(error?.response?.data?.message ?? 'خطا در برقراری ارتباط');

			transactions.value = [];
		} finally {
			loading.value = false;
		}
	});
</script>

<template>
	<div class="transactions">
		<div v-if="loading" class="transactions__state--loading">
			<h2>در حال دریافت اطلاعات تراکنش ها...</h2>
		</div>
		<div v-else-if="error" class="transactions__state--error">
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
				:loading="loading"
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
	</div>
</template>

<style lang="scss" scoped>
	.transactions {
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
