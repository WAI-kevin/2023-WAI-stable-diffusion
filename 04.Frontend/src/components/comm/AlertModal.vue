<template>
  <!--메세지 모달창-->
  <div class="modal-container">
    <div class="box-modal">
      <div v-if="storeCommon.$state.modeAlert === 'error'" class="modal-tit">
        Warning!
      </div>
      <div class="modal-message">
        {{ storeCommon.$state.messageAlert }}
      </div>

      <!--  메시지 모달창 버튼 시작   -->
      <div
        v-if="storeCommon.$state.modeAlert === 'confirm'"
        class="alert btn-group-bottom"
      >
        <button
          type="button"
          class="btn btn-custom btn-custom-v1 js-modal-master-close"
          @click="onClickConfirm"
        >
          확인
        </button>
        <button
          type="button"
          class="btn btn-custom js-modal-master-close"
          @click="onClickCancle"
        >
          취소
        </button>
      </div>
      <!--  메시지 모달창 버튼 끝   -->

      <!--  경고/에러 모달창 버튼 시작   -->
      <button
        v-else
        type="button"
        class="btn-custom btn-modal js-modal-master-close"
        @click="onClickClose"
      >
        확인
      </button>
      <!--  경고/에러 모달창 버튼 끝   -->
    </div>
  </div>
</template>

<script setup>
import { useCommonStore } from '@/stores/useCommonStore';

const storeCommon = useCommonStore(); // 공통 store 선언

const emits = defineEmits(['confirm', 'close']);

// confirm 팝업 '확인' 버튼 클릭시
const onClickConfirm = async () => {
  emits('confirm');
  if (storeCommon.confirmExec) {
    await storeCommon.confirmExec();
  }
};

// confirm 팝업 '취소' 버튼 클릭시
const onClickCancle = async () => {
  emits('close');
  if (storeCommon.cancleExec) {
    await storeCommon.cancleExec();
  }
};

// warning, error 팝업 '확인' 버튼 클릭시
const onClickClose = async () => {
  emits('close');
  if (storeCommon.closeExec) {
    await storeCommon.closeExec();
  }
};
</script>

<style scoped>
.alert.btn-group-bottom {
  justify-content: center;
}
</style>
