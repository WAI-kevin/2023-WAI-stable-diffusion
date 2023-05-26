<template>
  <section class="error errorgroupware">
    <div class="container">
      <div class="txt-group">
        <div class="txt">403 FORBIDDEN</div>
        <div class="txt2">
          죄송합니다. 권한이 없습니다. <br />사용자 등록 후 접근하시기 바랍니다.
        </div>
        <router-link to="/" class="btn">홈으로</router-link>
      </div>

      <img src="@/assets/img/img_error1.svg" alt=" " class="img-error" />
    </div>
  </section>
</template>

<script setup>
const props = defineProps({
  error: Object,
});
</script>

<style scoped></style>
