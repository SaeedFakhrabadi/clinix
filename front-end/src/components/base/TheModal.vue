<script setup>
	const props = defineProps({
		text: {
			type: String,
			required: true,
		},
		submitLabel: {
			type: String,
			default: 'تایید',
		},
	});

	const emit = defineEmits(['submit', 'close']);

	const close = () => emit('close');
	const submit = () => emit('submit');
</script>

<template>
	<div class="modal" @click="close">
		<form class="modal__container" @click.stop>
			<p class="modal__text">{{ text }}</p>
			<slot name="content"></slot>
			<div class="modal__buttons">
				<TheButton type="cancel" label="لغو" @click="close" />
				<TheButton type="submit" :label="submitLabel" @click="submit" />
			</div>
		</form>
	</div>
</template>

<style lang="scss" scoped>
	.modal {
		position: fixed;
		width: 100vw;
		height: 100vh;
		top: space(0);
		left: space(0);
		z-index: 10;
		background-color: #00000088;
		@include flexbox();

		&__container {
			width: 30%;
			background-color: var(--primary-700);
			box-shadow: space(0) space(0) space(5) var(--text-500);
			padding: space(14);
			border-radius: space(14);
			@include flexbox(column, center, center, space(6));

			@media (max-width: $lg) {
				width: 40%;
			}
			@media (max-width: $md) {
				width: 50%;
			}
			@media (max-width: $sm) {
				width: 80%;
			}
		}

		&__text {
			color: var(--text-900);
		}

		&__buttons {
			width: 100%;
			@include flexbox(row, center, center, space(6), nowrap);
		}
	}
</style>
