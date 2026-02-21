<script setup>
	import { ref, computed, onMounted } from 'vue';
	import { useRouter } from 'vue-router';
	import { useToast } from 'vue-toastification';
	import { useForm, useField } from 'vee-validate';
	import { storeToRefs } from 'pinia';
	import { profileSchema } from '@/schemas';
	import { editProfile } from '@/services/auth';
	import { doctorDetails } from '@/services/doctors';
	import { useCurrentUserStore } from '@/stores/currentUser';
	import { toPersianDigits } from '@/utils/toPersianDigits';
	import { addCommas } from '@/utils/addCommas';

	const router = useRouter();
	const toast = useToast();

	const loading = ref(true);
	const loadingError = ref(null);

	const currentUserStore = useCurrentUserStore();
	const { currentUser } = storeToRefs(currentUserStore);

	const doctor = ref({});

	const isPatient = computed(
		() => currentUser.value?.role?.value === 'PATIENT',
	);
	const isDoctor = computed(() => currentUser.value?.role?.value === 'DOCTOR');

	const startHour = ref(0);
	const endHour = ref(0);

	const HOURS = [
		{ label: 8, value: 8 },
		{ label: 9, value: 9 },
		{ label: 10, value: 10 },
		{ label: 11, value: 11 },
		{ label: 12, value: 12 },
		{ label: 13, value: 13 },
		{ label: 14, value: 14 },
		{ label: 15, value: 15 },
		{ label: 16, value: 16 },
		{ label: 17, value: 17 },
		{ label: 18, value: 18 },
		{ label: 19, value: 19 },
		{ label: 20, value: 20 },
		{ label: 21, value: 21 },
		{ label: 22, value: 22 },
	];

	const { handleSubmit } = useForm({
		validationSchema: profileSchema,
		initialValues: {
			name: '',
			email: '',
			phoneNumber: '',
		},
	});

	const role = ref('')
	const { value: name, errorMessage: nameError } = useField('name');
	const { value: email, errorMessage: emailError } = useField('email');
	const { value: phoneNumber, errorMessage: phoneNumberError } =
		useField('phoneNumber');

	const onSubmit = async () => {
		const toastId = toast.info('...در حال ثبت اطلاعات', {
			timeout: false,
			closeOnClick: false,
		});

		try {
			const payload = {
				username: name.value,
				email: email.value,
				phonenumber: phoneNumber.value,
			};
			const response = await editProfile(payload);

			currentUser.value.name = name.value;
			currentUser.value.email = email.value;
			currentUser.value.phoneNumber = phoneNumber.value;

			toast.dismiss(toastId);
			toast.success(response?.data?.message);
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

			toast.dismiss(toastId);
			toast.error(error?.response?.data?.message ?? 'خطا در برقراری ارتباط');
		}
	};

	const submitForm = handleSubmit(onSubmit);

	const editSchedule = async () => {
		const toastId = toast.info('...در حال ثبت اطلاعات', {
			timeout: false,
			closeOnClick: false,
		});

		try {
			if (Number(startHour.value) >= Number(endHour.value)) {
				toast.dismiss(toastId);
				toast.error('!ساعت پایان کار نباید قبل از ساعت شروع کار باشد');
				return;
			}

			const payload = {
				start_working_hour: String(startHour.value).padStart(2, '0') + ':00:00',
				end_working_hour: String(endHour.value).padStart(2, '0') + ':00:00',
			};

			const response = await editProfile(payload);

			toast.dismiss(toastId);
			toast.success(response?.data?.message);
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

			toast.dismiss(toastId);
			toast.error(error?.response?.data?.message ?? 'خطا در برقراری ارتباط');
		}
	};

	const setDefaultInfo = () => {
		role.value = currentUser.value.role?.label;
		name.value = currentUser.value?.name;
		email.value = currentUser.value?.email;
		phoneNumber.value = currentUser.value?.phoneNumber;
	};

	onMounted(async () => {
		if (isPatient.value) setDefaultInfo();
		if (isDoctor.value) {
			loading.value = true;
			try {
				const response = await doctorDetails(currentUser.value?.did);
				doctor.value = response.data;

				startHour.value = doctor.value?.start_working_hour;
				endHour.value = doctor.value?.end_working_hour;

				loading.value = false;
			} catch (error) {
				console.error('Error : ', error?.response?.data || error?.message);

				toast.error(error?.response?.data?.message ?? 'خطا در برقراری ارتباط');

				loading.value = false;
				loadingError.value = true;
			}
		}
	});
</script>

<template>
	<div class="profile">
		<h2 class="profile__title">اطلاعات شخصی</h2>
		<form v-if="isPatient" class="profile__form" @submit.prevent="submitForm">
			<div class="profile__sections-patient">
				<section class="profile__section-patient">
					<TheInput
						v-model="name"
						label="نام"
						icon-name="user"
						:error-message="nameError"
					/>
					<TheInput
						v-model="role"
						label="نقش"
						icon-name="user-role"
						is-disabled
					/>
				</section>
				<section class="profile__section-patient">
					<TheInput
						v-model="email"
						label="ایمیل"
						type="email"
						icon-name="email"
						:error-message="emailError"
					/>
					<TheInput
						v-model="phoneNumber"
						label="شماره تماس"
						icon-name="phone"
						digits-only
						:error-message="phoneNumberError"
					/>
				</section>
			</div>
			<section class="profile__section-buttons">
				<TheButton
					type="cancel"
					label="لغو تغییرات"
					@click.prevent="setDefaultInfo"
				/>
				<TheButton type="submit" label="ثبت اطلاعات شخصی" />
			</section>
		</form>
		<div v-if="isDoctor" class="profile__container">
			<div class="profile__sections-doctor">
				<section class="profile__section-doctor">
					<div class="profile__item item">
						<span class="item__label">نام:</span>
						<h3 class="item__value">دکتر {{ currentUser?.name }}</h3>
					</div>
					<div class="profile__item item">
						<span class="item__label">شماره تلفن:</span>
						<h3 class="item__value">
							{{ toPersianDigits(currentUser?.phoneNumber) }}
						</h3>
					</div>
				</section>
				<section class="profile__section-doctor">
					<div class="profile__item item">
						<span class="item__label">ایمیل:</span>
						<h3 class="item__value">{{ currentUser?.email }}</h3>
					</div>
				</section>
			</div>
		</div>
		<h2 v-if="isDoctor" class="profile__title">اطلاعات پزشکی</h2>
		<div v-if="isDoctor" class="profile__container">
			<div class="profile__sections-doctor">
				<section class="profile__section-doctor">
					<div class="profile__item item">
						<span class="item__label">تخصص:</span>
						<h3 class="item__value">{{ doctor?.field }}</h3>
					</div>
					<div class="profile__item item">
						<span class="item__label">سابقه کار:</span>
						<h3 class="item__value">
							{{ toPersianDigits(doctor?.experience || 0) }} سال
						</h3>
					</div>
				</section>
				<section class="profile__section-doctor">
					<div class="profile__item item">
						<span class="item__label">قیمت ویزیت (ساعت):</span>
						<h3 class="item__value">{{ addCommas(doctor?.price) }}</h3>
					</div>
					<div class="profile__item item">
						<span class="item__label">میانگین امتیازات دریافتی:</span>
						<h3 v-if="doctor?.score !== 0" class="item__value">
							{{ toPersianDigits(`${doctor?.score} از 5`) }}
						</h3>
						<h3 v-else class="item__value">بدون امتیاز</h3>
					</div>
				</section>
				<section class="profile__section-doctor">
					<div class="profile__item item">
						<span class="item__label">موقعیت مطب:</span>
						<h3 class="item__value">{{ doctor?.location }}</h3>
					</div>
				</section>
			</div>
		</div>
		<h2 v-if="isDoctor" class="profile__title">ساعت کاری</h2>
		<form v-if="isDoctor" class="profile__form" @submit.prevent="editSchedule">
			<div class="profile__section-patient">
				<TheSelect
					label="ساعت شروع کار"
					icon-name="clock"
					v-model="startHour"
					:options="HOURS"
				/>
				<TheSelect
					label="ساعت پایان کار"
					icon-name="clock"
					v-model="endHour"
					:options="HOURS"
				/>
			</div>
			<TheButton label="ثبت ساعات کاری جدید" type="submit" />
		</form>
	</div>
</template>

<style lang="scss" scoped>
	.profile {
		&__title {
			color: var(--text-900);
			padding-right: space(4);
			border-right: space(4) solid var(--title-100);
		}

		&__form {
			width: 100%;
			@include flexbox(column, center, center, space(10));
		}

		&__sections-patient {
			width: 100%;
			@include flexbox(column, center, center, space(0));
		}

		&__section-patient {
			width: 100%;
			@include flexbox(row, center, start, space(10), nowrap);

			@media (max-width: $md) {
				@include flexbox(column, center, start, space(0));
			}
		}

		&__section-buttons {
			width: 100%;
			@include flexbox(row, center, start, space(10), nowrap);

			@media (max-width: $md) {
				@include flexbox(column, center, start, space(14));
			}
		}

		&__container {
			width: 100%;
			padding-bottom: space(10);
			@include flexbox(column, center, start, space(10));
		}

		&__sections-doctor {
			width: calc(100% - space(12));
			background-color: var(--primary-700);
			box-shadow: space(0) space(0) space(5) var(--text-500);
			padding: space(6);
			border-radius: space(14);
			@include flexbox(column, center, center, space(4));

			@media (max-width: $lg) {
				@include flexbox(column, center, start, space(0));
			}
		}

		&__section-doctor {
			width: 100%;
			@include flexbox(row, center, start, space(0), nowrap);

			@media (max-width: $lg) {
				@include flexbox(column, center, start, space(0));
			}
		}

		.item {
			width: 100%;
			@include flexbox(row, start, center, space(2), nowrap);

			&__label {
				font-size: space(10);
				color: var(--text-400);
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
