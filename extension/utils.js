export default
  function get_site(url){
    if (url.match(/https:\/\/mangatx\.com\/manga\/.+\/.+\//)){
      return 'mangatx'
    }
    else if(url.match(/https:\/\/chapmanganato\.com\/manga.+\/chapter-.+/)){
      return 'readmanganato'
    }
    else if(url.match(/https:\/\/mangakakalot\.com\/chapter\/.+\/.+/)){
      return 'mangakakalot'
    }
    else if(url.match(/https:\/\/asura\.gg\/.*/)){
      return 'asurascans'
    }
    else if (url.match(/https:\/\/lhtranslation\.net\/manga\/.*\/.*/)){
        return "lhtranslation"
    }
    else return 'undefined'
  }
