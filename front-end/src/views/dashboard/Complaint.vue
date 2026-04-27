<script setup>
	import { useForm, useField } from 'vee-validate';
	import { complaintSchema } from '@/schemas';
	import { createComplaint } from '@/services/complaint';
	import { useToast } from 'vue-toastification';

	const toast = useToast();

	const { handleSubmit } = useForm({
		validationSchema: complaintSchema,
		initialValues: {
			subject: '',
			message: '',
		},
	});

	const { value: subject, errorMessage: subjectError } = useField('subject');
	const { value: message, errorMessage: messageError } = useField('message');

	const onSubmit = async () => {
		const toastId = toast.info('...در حال ثبت اطلاعات', {
			timeout: false,
			closeOnClick: false,
		});

		try {
			const response = await createComplaint(subject.value, message.value);

			toast.dismiss(toastId);
			toast.success(response?.data?.message);
		} catch (error) {
			console.error('Error : ', error?.response?.data || error?.message);

			toast.dismiss(toastId);
			toast.error(error?.response?.data?.message ?? 'خطا در برقراری ارتباط');
		}
	};
	const submitForm = handleSubmit(onSubmit);
</script>

<template>
	<div class="complaint">
		<TheTitle label="پشتیبانی و ثبت انتقادات و پیشنهادات" />
		<form class="complaint__form" @submit.prevent="submitForm">
			<TheInput
				icon-name="id-card"
				v-model="subject"
				:error-message="subjectError"
				label="موضوع"
				placeholder="لطفا موضوع انتقاد یا پیشنهاد خود را وارد کنید"
			/>
			<TheInput
				type="textarea"
				icon-name="message-check"
				v-model="message"
				:error-message="messageError"
				label="ثبت انتقاد یا پیشنهاد"
				placeholder="هرچه می خواهد دل تنگت بگو :)"
			/>
			<TheButton
				type="submit"
				label="ثبت انتقاد یا پیشنهاد"
				class="complaint__button"
			/>
		</form>
	</div>
</template>

<style lang="scss" scoped>
	.complaint {
		&__form {
			width: 100%;
			@include flexbox(column, center, start, space(0), nowrap);
		}

		&__button {
			margin-top: space(10);
		}
	}
</style>
