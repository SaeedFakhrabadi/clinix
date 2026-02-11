<script setup>
	import { toPersianDigits } from '@/utils/toPersianDigits';

	const props = defineProps({
		headers: {
			type: Array,
			required: true,
		},
		rows: {
			type: Array,
			required: true,
		},
		loading: {
			type: Boolean,
			default: false,
		},
	});
</script>

<template>
	<div class="the-table">
		<div v-if="loading" class="the-table__state">
			<h2>در حال دریافت اطلاعات...</h2>
		</div>
		<div v-else-if="!rows?.length" class="the-table__state">
			<h2>اطلاعاتی برای نمایش وجود ندارد!</h2>
		</div>
		<table v-else class="the-table__table table"">
			<thead class="table__head">
				<tr>
					<th class="table__head-cell">
						<h4>ردیف</h4>
					</th>
					<th
						v-for="header in headers"
						:key="header.value"
						class="table__head-cell"
					>
						<h4>{{ header.label }}</h4>
					</th>
				</tr>
			</thead>
			<tbody class="table__body">
				<tr v-for="(row, index) in rows" :key="row.id ?? index">
					<td class="table__body-cell">
						<h4>{{ toPersianDigits(index + 1) }}</h4>
					</td>
					<td
						v-for="header in headers"
						:key="header.value"
						class="table__body-cell"
					>
						<h4>{{ toPersianDigits(row[header.value] )}}</h4>
					</td>
				</tr>
			</tbody>
		</table>	
	</div>
</template>

<style scoped lang="scss">
	.the-table {
		width: 100%;

		&__state {
			color: var(--text-500);
			@include flexbox();
		}

		.table {
			width: 100%;
			border-collapse: collapse;

			&__head {
				background-color: var(--primary-300);
			}

			&__head-cell {
				color: var(--text-900);
				padding: space(4);
				border: space(1) solid var(--text-500);
			}

			&__body-cell {
				color: var(--text-900);
				padding: space(4);
				border: space(1) solid var(--text-500);
				text-align: center;
			}

			&__body {
				tr:nth-child(odd) .table__body-cell {
					background-color: var(--bg-900);
				}

				tr:nth-child(even) .table__body-cell {
					background-color: var(--bg-600);
				}
			}
		}
	}
</style>
