<template>
    <div class="container">
        <header class="header-image"></header>
        <div class="body">
            <div class="title">{{ $t('methodology.title') }}</div>
            <i18n-t keypath="methodology.desc1" tag="p">
            <a href="https://twitter.com/jjansasds" target="_blank">@jjansasds</a>
            </i18n-t>

            <p>{{ $t('methodology.desc2') }}</p>

            <i18n-t keypath="methodology.desc3" tag="p">
            <a href="mailto:vsi@danesjenovdan.si" target="_blank">{{ $t('methodology.mailLink') }}</a>
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