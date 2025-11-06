<script setup>
  import { ref } from 'vue';
  import TheInput from '@/components/base/TheInput.vue';

  // داده های فرم
  const name = ref('');
  const email = ref('');
  const phone = ref('');
  const age = ref('');
  const password = ref('');
  const confirmPassword = ref('');

  // ارورها
  const errors = ref({
    name: '',
    email: '',
    phone: '',
    age: '',
    password: '',
    confirmPassword: '',
  });

  // اعتبارسنجی ساده هنگام submit
  const validate = () => {
    let valid = true;
    errors.value.name = name.value.trim() ? '' : 'نام الزامی است';
    errors.value.email = /\S+@\S+\.\S+/.test(email.value) ? '' : 'ایمیل معتبر نیست';
    errors.value.phone = /^\d{10,15}$/.test(phone.value) ? '' : 'شماره تلفن معتبر نیست';
    errors.value.password = password.value.length >= 6 ? '' : 'رمز عبور باید حداقل 6 کاراکتر باشد';
    errors.value.confirmPassword = confirmPassword.value === password.value ? '' : 'تکرار رمز عبور اشتباه است';

    Object.values(errors.value).forEach((e) => {
      if (e) valid = false;
    });
    return valid;
  };

  const handleSubmit = () => {
    if (validate()) {
      alert('ثبت‌نام با موفقیت انجام شد!');
      // اینجا میتونی API call بزنی
    }
  };
</script>

<template>
  <form @submit.prevent="handleSubmit" class="sign-up-form">
    <h2 class="sign-up-form__title">ثبت نام</h2>
    <div class="sign-up-form__row">
      <TheInput label="نام" placeholder="نام خود را وارد کنید" v-model="name" :error-message="errors.name" />
      <TheInput label="ایمیل" placeholder="ایمیل خود را وارد کنید" v-model="email" :error-message="errors.email" />
    </div>
    <div class="sign-up-form__row">
      <TheInput label="شماره تلفن" placeholder="شماره تلفن" v-model="phone" :error-message="errors.phone" />
      <TheInput label="سن" placeholder="به طور مثال: 20" v-model="age" :error-message="errors.age" />
    </div>
    <div class="sign-up-form__row">
      <TheInput
        label="رمز عبور"
        type="password"
        placeholder="رمز عبور"
        v-model="password"
        :error-message="errors.password" />
      <TheInput
        label="تکرار رمز عبور"
        type="password"
        placeholder="رمز عبور را دوباره وارد کنید"
        v-model="confirmPassword"
        :error-message="errors.confirmPassword"
    /></div>

    <button type="submit">ثبت‌نام</button>
  </form>
</template>

<style scoped lang="scss">
  .sign-up-form {
    background-color: var(--primary-500);
    padding: space(20);
    border-radius: space(10);
    width: 300px;
    margin: 0 auto;
    @include flexbox(column, start, center, space(4));

    &__title {
      background-image: linear-gradient(90deg, var(--primary-500), var(--primary-900));
      padding-inline: space(6);
      border-top-right-radius: space(6);
      border-bottom-right-radius: space(6);
      color: var(--text-900);
    }

    &__row {
      @include flexbox(row, space-between, center, space(10), nowrap);
    }

    button {
      width: 100%;
      padding: 10px;
      background-color: var(--secondary-100);
      color: var(--text-900);
      border: none;
      border-radius: space(6);
      cursor: pointer;
      &:hover {
        background-color: var(--secondary-500);
      }
    }
  }
</style>
