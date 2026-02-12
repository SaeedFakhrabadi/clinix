<script setup>
	import { ref, onMounted, onUnmounted } from 'vue';

	const props = defineProps({
		initialMinutes: {
			type: Number,
			default: 5,
		},
	});

	const timer = ref(`05:00`);
	let timerInterval = null;

	const startTimer = () => {
		let totalSeconds = props.initialMinutes * 60;

		timerInterval = setInterval(() => {
			totalSeconds--;

			if (totalSeconds < 0) {
				clearInterval(timerInterval);
				timer.value = '00:00';
				return;
			}

			const minutes = Math.floor(totalSeconds / 60);
			const seconds = totalSeconds % 60;
			timer.value = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
		}, 1000);
	};

	onMounted(() => {
		startTimer();
	});

	onUnmounted(() => {
		clearInterval(timerInterval);
	});
</script>

<template>
	<div class="countdown-timer">
		<router-link
			v-if="timer === '00:00'"
			class="countdown-timer__link"
			:to="{ name: 'RecoveryPassword' }"
		>
			<h5>درخواست ارسال مجدد کد تایید</h5>
		</router-link>
		<h5 v-else class="countdown-timer__timer">{{ timer }}</h5>
	</div>
</template>

<style lang="scss" scoped>
	.countdown-timer {
		position: absolute;
		left: space(0);
		top: space(0);
		user-select: none;

		&__timer {
			color: var(--danger-500);
		}

		&__link {
			text-decoration: underline;
			color: var(--text-500);
		}
	}
</style>
