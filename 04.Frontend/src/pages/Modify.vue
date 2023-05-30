<template>
  <div>
    <v-textarea
      class="pt-30"
      label="Enter your prompt here"
      variant="solo"
      v-model="this.prompt"
      rows="4"
    ></v-textarea>
    <v-file-input
      label="Upload Image"
      color="white"
      bg-color="rgba(166, 182, 226, 1)"
      ref="fileAdd"
      v-model="this.inputImg"
      @update:modelValue="inputChng()"
    ></v-file-input>
    <div class="d-flex grid-gap-15 mb-20">
      <v-autocomplete
        hide-details
        color="white"
        label="lighting and mood"
        :items="[
          '35mm',
          'sharp',
          'low poly 3d render',
          'golden hour',
          'sunny sky',
          'hyper realistic',
          'epic scale',
          'sense of awe',
          'hypermaximalist',
          'insane level of details',
          'artstation HQ',
          '80mm',
          'photoshopped',
          'insanely detailed',
          'intricate',
          'brush effect',
          'macro',
          'precise correct anatomy',
          'matte painting',
        ]"
        bg-color="rgba(166, 182, 226, 1)"
      ></v-autocomplete>
      <v-autocomplete
        hide-details
        color="white"
        label="artistic style and mediums"
        :items="[
          'Pablo Picasso',
          'Van Gogh',
          'Da Vinci',
          'Hokusai',
          'Manga',
          'fantasy',
          'minimalism',
          'abstract',
          'graffiti',
          'Digital art',
          'digital painting',
          'color page',
          'featured on pixiv (for anime/manga)',
          'trending on artstation',
          'precise line-art',
          'tarot card',
          'character design',
          'concept art',
          'symmetry',
          'golden ratio',
          'evocative',
          'award winning',
          'shiny',
          'smooth',
          'surreal',
          'divine',
          'celestial',
          'elegant',
          'oil painting',
          'soft',
          'fascinating',
          'fine art',
          'Oil on canvas',
          'watercolour',
          'sketch',
          'photography',
          'Isometric',
          'pixar',
          'scientific',
          'comic',
        ]"
        bg-color="rgba(166, 182, 226, 1)"
      ></v-autocomplete>
      <v-autocomplete
        hide-details
        color="white"
        label="picture style and quality"
        :items="[
          'ultra wide-angle',
          'wide-angle',
          'aerial view',
          'massive scale',
          'street level view',
          'landscape',
          'panoramic',
          'bokeh',
          'fisheye',
          'dutch angle',
          'low angle',
          'extreme long-shot',
          'long shot',
          'close-up',
          'extreme close-up',
          'highly detailed',
          '4k',
          '8k uhd',
          'studio quality',
          'polaroid',
          '100mm',
          'film photography',
          'dslr',
          'cinema4d',
          'movie concept arthighly detailed',
          'grainy',
          'unreal engine',
          'octane render',
          'vray',
          'houdini render',
          'quixel megascans',
          'depth of field (or dof)',
          'arnold render',
          'raytracing',
          'cgi',
          'lumen reflections',
          'cgsociety',
          'realistic',
          'ultra realistic',
          'volumetric fog',
          'overglaze',
          'analog photo',
        ]"
        bg-color="rgba(166, 182, 226, 1)"
      ></v-autocomplete>
      <v-autocomplete
        hide-details
        color="white"
        label="Theme"
        :items="['Theme1', 'Theme2', 'Theme3']"
        bg-color="rgba(166, 182, 226, 1)"
      ></v-autocomplete>
    </div>
    <div class="mb-15 text-right">
      <v-btn rounded="xl" size="x-large" class="btn-style-2">RUN</v-btn>
    </div>
    <v-card>
      <v-card-text
        ><v-textarea
          label="Your Prompt"
          variant="underlined"
          readonly
          v-model="this.resultPrompt"
        ></v-textarea>
      </v-card-text>
      <div id="painterro"></div
    ></v-card>
    <div class="d-flex pt-30 justify-content-space-between">
      <v-btn variant="flat" rounded="xl" class="btn-style-2">SHARE</v-btn>
      <v-btn variant="flat" rounded="xl" class="btn-style-2">RESET</v-btn>
    </div>
    <!-- <v-btn @click="painterro.show()">편집 버튼</v-btn> -->
  </div>
</template>
<script>
import Painterro from 'painterro';
export default {
  data() {
    return {
      resultPrompt:
        'The Woodman set to work at once, and so sharp was his axe that the tree was soon chopped nearly through.',
      painterro: null,
      prompt: '',
      inputImg: null,
    };
  },
  mounted() {},
  methods: {
    inputChng: function () {
      if (this.painterro) {
        console.log('durldurldjdjdjdjdj');
        this.painterro = null;
      }
      this.painterro = Painterro({
        id: 'painterro',
        hiddenTools: ['arrow', 'text', 'close', 'bucket'],
        backplateImgUrl: window.URL.createObjectURL(this.inputImg[0]),
        colorScheme: {
          main: '#f8f8f8',
          control: '#d5d5d5',
          controlContent: '#434649',
        },
        saveHandler: (image, done) => {
          var a = document.createElement('a');
          const file = image.asBlob();
          const downloadUrl = window.URL.createObjectURL(file);
          a.href = downloadUrl;
          a.download = 'down';
          document.body.appendChild(a);
          a.click();
          document.body.removeChild(a);
          done(true);
        },
      });
      this.painterro.show();
    },
  },
};
</script>
