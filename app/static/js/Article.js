export default class Article {

  constructor() {
    this.body = document.querySelector("body");

    this.getArticleURL = document.getElementById("getArticleURL");
    this.getArticleBtn = document.getElementById("getArticleBtn");
    this.article = document.getElementById("article");
    this.hero = document.getElementById("hero");
    this.heroTitle = document.getElementById("hero__title");
    this.heroForm = document.getElementById("hero__form");

    this.loader = {}

    this.segmentsList = {}

    this.statusMonitor = {}
    this.statusMonitorTitle = {}
    this.statusMonitorStatus = {}
    this.stautsMonitorProgress = {}
    this.stautsMonitorProgressValue = {}
    this.video = {}


    this.getArticleBtn.addEventListener("click", (e)=> {
      // Обработчик клика на кнопке "Отправить"

      this.setVideo();
      this.article.innerHTML = "";
      this.initLoader();
      this.setTask();

    });


    this.getArticleURL.addEventListener("focus", ()=> {
      // Если нажали на поле ввода адреса, уменьшается
      // форма и заголовок

      this.heroTitle.classList.add("hero__title_small");
    });
  }


  setVideo() {
    this.video = {
      pk: this.getVideoId(this.getArticleURL.value)
    }
  }


  async setTask() {
    // Первичный запрос на постановку задачи

    let response = await fetch('/tasks', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json;charset=utf-8'
      },
      body: JSON.stringify(this.video)
    });
    let result = await response.json();

    this.body.removeChild(this.loader);
    this.getTaskInfo(result);
  }


  getTaskInfo(result) {
    // Проверяем, если записи в базе нет
    if (result.status != 200) {

      // !
      console.log("not ready");
      // Выводим монитор статуса
      // this.article.innerHTML = "";
      this.createStatusMonitor();
      this.updateStatusMonitor(result);

      // Запускаем проверку статусов каждые 2с
      let timerId = setInterval(()=>{
        this.checkTaskStatus(timerId);
      }, 5000);
    }

    // Если запись есть, выполняем запрос на получение
    // статьи из базы
    else {
      this.getArticle();
    }
  }


  async checkTaskStatus(timerId) {
    // Функция проверки статуса задачи

    let response = await fetch('/tasks/'+this.video.pk, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json;charset=utf-8'
      }
    });
    let result = await response.json();

    this.updateStatusMonitor(result);

    // Если пришел статус 200 (статья готова)
    if (result.status == 200) {
      // Останавливаем проверку
      clearInterval(timerId);
      // Запрашиваем статью
      this.getArticle();
      // Удаляем монитор
      this.body.removeChild(this.statusMonitor);
    }
  }


  async getArticle() {
    // Запрос статьи из базы

    let response = await fetch('/articles/'+this.video.pk, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json;charset=utf-8'
      }
    });
    let result = await response.json();

    // Отрисовываем статью
    this.renderArticle(result);
  }


  createStatusMonitor() {
    // Первичная инициализация монитора статусов задачи

    this.statusMonitor = document.createElement("div");
    this.statusMonitor.classList.add("message-box");

    this.statusMonitorTitle = document.createElement("h2");
    this.statusMonitorTitle.classList.add("message-box__title");
    this.statusMonitorTitle.innerHTML = "Статус задачи";

    this.statusMonitorStatus = document.createElement("h3");
    this.statusMonitorStatus.classList.add("message-box__status");

    this.stautsMonitorProgress = document.createElement("div");
    this.stautsMonitorProgress.classList.add("message-box__progress");

    this.stautsMonitorProgressValue = document.createElement("div");
    this.stautsMonitorProgressValue.classList.add("message-box__progress-value")

    this.body.append(this.statusMonitor);
    this.statusMonitor.append(this.statusMonitorTitle);
    this.statusMonitor.append(this.statusMonitorStatus);
    this.statusMonitor.append(this.stautsMonitorProgress);
    this.stautsMonitorProgress.append(this.stautsMonitorProgressValue);

  }


  updateStatusMonitor(result) {
    // Перерисовка данных о состоянии задачи

    this.statusMonitorStatus.innerHTML = `${this.convertStatus(result.status)}`;
    if (result.progress == 0) {
      this.stautsMonitorProgressValue.classList.remove("message-box__progress-value");
      this.stautsMonitorProgressValue.classList.add("message-box__progress-value_unknown");
      this.stautsMonitorProgressValue.style.width = "100%";
    }
    else {
      this.stautsMonitorProgressValue.classList.remove("message-box__progress-value_unknown");
      this.stautsMonitorProgressValue.classList.add("message-box__progress-value");
      this.stautsMonitorProgressValue.style.width = `${result.progress}%`;
    }

    // ! console
    console.log(result.status);
  }


  createSegment(segment, pk) {
    const node = document.createElement("div");
    node.classList.add("segment-elem");
    node.innerHTML = `<div class="segment-elem__timecode">
                        <span class="material-symbols-outlined">
                          timer
                        </span>
                        <a href="https://www.youtube.com/watch?v=${pk}&t=${Math.floor(segment.start)}" class="timecode-ref" target="_blank">
                          ${this.convert_time(segment.start)}
                        </a>
                      </div>
                      <div class="segment-elem__content">
                        <div class="segment-elem__img-wrapper">
                          ${this.getImages(segment.images)}
                        </div>
                        <h3 class="subtitle">${segment.title}</h3>
                        <div class="segment-elem__text" title="${segment.text}" contenteditable="true">
                          ${segment.edited_text}
                        </div>
                      </div>`;

    return node;
  }

  getImages(images) {
    let node = ""
    images.forEach(image => {
      node += `<div><a href="app/static/images/screenshots/${image}" target="_blank"><img class="segment-elem__img" src="app/static/images/screenshots/${image}"/></a></div>`;
    });
    return node;
  }

  createArtilceTitle(title) {
    const node = document.createElement("h2");
    node.setAttribute("contenteditable", "true");
    node.classList.add("article-title");
    node.innerHTML = title;
    return node;
  }

  createArticleAbstract(abstract) {
    const node = document.createElement("p");
    node.setAttribute("contenteditable", "true");
    node.classList.add("article-abstract");
    node.innerHTML = abstract;
    return node;
  }

  createSegmentsList() {
    const node = document.createElement("div");
    node.classList.add("segmentsList");

    return node;
  }


  renderArticle(article) {
    // Отрисовываем статью

    this.article.append(this.createArtilceTitle(article.title));

    this.article.append(this.createArticleAbstract(article.abstract));

    this.segmentsList = this.createSegmentsList();
    this.article.append(this.segmentsList);

    article.paragraphs.forEach(segment => {
      this.segmentsList.append(this.createSegment(segment, this.video.pk));
    });

  }


  convert_time(time) {
    // Конвертируем время в удобочитаемый формат

    time = Math.floor(time)
    let minute = Math.floor(time/60)
    let sec = time%60
    if (sec < 10) sec = '0' + sec
    return `${minute}:${sec}`
  }


  getVideoId(url) {
    // Вытаскиваем id-видео из адреса

    let id = -1;
    const index = url.indexOf('v=');

    if (index != -1) {
      id = url.substr(index+2, 11);
    }

    return id;
  }


  initLoader() {
    // Запуск индикатора запроса

    this.loader = document.createElement("div");
    this.loader.classList.add("loader")
    this.loader.innerHTML = `
    <div class="loader__indicator"></div>
    `;

    this.body.append(this.loader);

  }


  convertStatus(status) {
    // Очеловечивание статусов

    switch(status) {
      case 0:
        status = `<span class="material-symbols-outlined message-box-status-icon">
                    follow_the_signs
                  </span>
                  Мы в очереди`;
        break;
      case 1:
        status = `<span class="material-symbols-outlined message-box-status-icon">
                    speech_to_text
                  </span>
                  Получаем субтитры от YouTube`;
        break;
      case 2:
        status = `<span class="material-symbols-outlined message-box-status-icon">
                    format_paragraph
                  </span>
                  Обрабатываем субтитры`;
        break;
      case 3:
        status = `<span class="material-symbols-outlined message-box-status-icon">
                    draw
                  </span>
                  Пошла возня... Переписываем текст`;
        break;
      case 4:
        status = `<span class="material-symbols-outlined message-box-status-icon">
                    smart_display
                  </span>
                  Скачиваем видео`;
        break;
      case 5:
        status = `<span class="material-symbols-outlined message-box-status-icon">
                    photo_library
                  </span>
                  Делаем скриншоты`;
        break;
      case 6:
        status = `<span class="material-symbols-outlined message-box-status-icon">
                    rocket_launch
                  </span>
                  Готовим статью к отправке`;
        break;
      case 200:
        status = `<span class="material-symbols-outlined message-box-status-icon">
                    sentiment_satisfied
                  </span>
                  Готово`;
        break;
      default:
        status = `<span class="material-symbols-outlined message-box-status-icon">
                    sentiment_dissatisfied
                  </span>
                  Что-то пошло не так`;
        break;
    }

    return status;
  }

}
