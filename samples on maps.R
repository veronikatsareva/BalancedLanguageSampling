install.packages("lingtypology")
library(lingtypology)

# The Original Sample
df_original <- data.frame(language = c("Basque",
                              "Czech",
                              "Russian",
                              "Hindi",
                              "Estonian",
                              'Spanish',
                              "French",
                              "Latin",
                              "Polish",
                              "German",
                              "Finnish",
                              "Urdu",
                              "Latvian",
                              "Norwegian",
                              "Western Farsi",
                              "Japanese",
                              "Croatian Standard",
                              "Slovenian",
                              "English",
                              "Standard Hebrew",
                              "Mandarin Chinese",
                              "Standard Indonesian",
                              "Serbian Standard",
                              "Slovak"))

map.feature(df_original$language, 
            label = df_original$language,
            color = "black",
            tile = "Esri.WorldGrayCanvas")

# The Balanced Sample
df_balanced <- data.frame(language = c("Afrikaans",
                                     "Eastern Armenian",
                                     "Basque",
                                     "Mandarin Chinese",
                                     'Georgian',
                                     "Greek",
                                     "Hungarian",
                                     'Standard Indonesian',
                                     "Irish",
                                     "Japanese",
                                     "Javanese",
                                     "Korean",
                                     "Latin",
                                     "Latvian",
                                     "Western Farsi",
                                     "Tamil",
                                     "Thai",
                                     "Vietnamese",
                                     "Hindi",
                                     "Finnish",
                                     "Turkish",
                                     "Arabic",
                                     "Russian",
                                     "Portuguese"))

map.feature(df_balanced$language, 
            label = df_balanced$language, 
            color = "black",
            tile = "Esri.WorldGrayCanvas")
