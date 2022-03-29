<template>
  <div class="container">
    <header class="header-image"></header>
    <div class="body">
      <div class="title">{{ $t('about.title') }}</div>
      <i18n-t keypath="about.desc1" tag="p">
        <i>{{ $t('projectName') }}</i>
      </i18n-t>
      <p>
        {{ $t('about.desc2') }}
      </p>
      <p>
        {{ $t('about.desc3') }}
      </p>
      <p>
        {{ $t('about.desc4') }}
      </p>

      <div class="subtitle">{{ $t('about.subtitle1') }}</div>
      <i18n-t keypath="about.desc5" tag="p">
        <a href="mailto:vsi@danesjenovdan.si">vsi@danesjenovdan.si</a>
      </i18n-t>

      <div class="subtitle">{{ $t('about.subtitle2') }}</div>
      <i18n-t keypath="about.desc6" tag="p">
        <a href="https://danesjenovdan.si/">{{ $t('djnd') }}</a>
        <a href="https://danesjenovdan.si/doniraj">{{ $t('about.donate') }}</a>
      </i18n-t>
      <i18n-t keypath="about.desc7" tag="p">
        <a href="https://www.stokto.com/">Stokto</a>
      </i18n-t>
    </div>
  </div>
</template>

<style scoped>
.header-image {
  line-height: 0;
  background: #44a58a;
  padding: 28.15% 0;
  background-image: url('/twito.png');
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center;
}

.container {
  max-width: 978px;
  margin: 0 auto;
  margin-bottom: 60px;
}

.body {
  background-color: white;
  color: black;
  text-align: left;
  padding: 60px 75px;
  font-size: 1.5rem;
}

@media (max-width: 767.98px) {
  .body {
    padding: 30px 20px;
  }
}

.title {
  font-size: 2.5rem;
  font-weight: bold;
  text-transform: uppercase;
  margin-bottom: 1.75rem;
  padding-right: 1.75rem;
}

.subtitle {
  text-transform: uppercase;
  font-size: 2rem;
  margin-top: 3rem;
  margin-bottom: 0.25rem;
}

p {
  line-height: 1.75em;
  margin: 0 0 0.75em;
}

p:last-child {
  margin: 0;
}

a {
  color: inherit;
}
</style>