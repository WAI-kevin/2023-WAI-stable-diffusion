import { defineStore } from 'pinia';

export const useCommonStore = defineStore('common', {
  state: () => ({
    modalAlert: false, // 알림창 show/hide 여부
    messageAlert: undefined, // 메시지
    modeAlert: undefined, // 모드 : 에러창(error), 메시지창(confirm), 경고창(default 값이 없음)
    actionAlert: undefined, // 확인 action
    confirmExec: undefined, // confirm 확인 클릭시 실행 함수
    cancleExec: undefined, // confirm 취소 클릭시 실행 함수
    closeExec: undefined, // error, warning 확인 클릭시 실행 함수
  }),
  actions: {
    showModalAlert(message, mode = '', confirm, cancle, close) {
      this.modalAlert = true;
      this.messageAlert = message;
      this.modeAlert = mode;
      this.actionAlert = undefined;
      confirm ? (this.confirmExec = confirm) : (this.confirmExec = undefined);
      cancle ? (this.cancleExec = confirm) : (this.cancleExec = undefined);
      close ? (this.closeExec = confirm) : (this.closeExec = undefined);
    },
    hideModalAlert(action) {
      this.modalAlert = false;
      this.messageAlert = undefined;
      this.modeAlert = undefined;
      if (action) this.actionAlert = action;
    },
    initAlert() {
      this.modalAlert = false;
      this.messageAlert = undefined;
      this.modeAlert = undefined;
      this.actionAlert = undefined;
    },
  },
  persist: true,
});
