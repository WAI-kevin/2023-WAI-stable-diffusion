<template>
  <section class="error">
    <div class="container">
      <div class="txt-group">
        <div class="txt">404 ERROR</div>
        <div class="txt2">
          죄송합니다. 페이지를 찾을 수 없습니다. <br />존재하지 않는 주소를
          입력하셨거나 <br />요청하신 페이지의 주소가 변경, 삭제되어 찾을 수
          없습니다.
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
