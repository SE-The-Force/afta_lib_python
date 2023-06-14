import re

class AmharicNormalizer:
    """
    Class representing an Amharic preprocessor.
    """

    @staticmethod
    def normalize(norm):
        substitutions = [
            ["ሀ", "ሃ"], ["ሐ", "ሃ"], ["ሓ", "ሃ"], ["ኅ", "ሃ"], ["ኻ", "ሃ"], ["ኃ", "ሃ"], ["ዅ", "ሁ"], ["ሗ", "ኋ"], ["ኁ", "ሁ"], ["ኂ", "ሂ"],
            ["ኄ", "ሄ"], ["ዄ", "ሄ"], ["ኅ", "ህ"], ["ኆ", "ሆ"], ["ሑ", "ሁ"], ["ሒ", "ሂ"], ["ሔ", "ሄ"], ["ሕ", "ህ"], ["ሖ", "ሆ"], ["ኾ", "ሆ"],
            ["ሠ", "ሰ"], ["ሡ", "ሱ"], ["ሢ", "ሲ"], ["ሣ", "ሳ"], ["ሤ", "ሴ"], ["ሥ", "ስ"], ["ሦ", "ሶ"], ["ዐ", "አ"], ["ዑ", "ኡ"], ["ዒ", "ኢ"],
            ["ዓ", "አ"], ["ኣ", "አ"], ["ዔ", "ኤ"], ["ዕ", "እ"], ["ዖ", "ኦ"], ["ፀ", "ጸ"], ["ፁ", "ጹ"], ["ጺ", "ፂ"], ["ጻ", "ፃ"], ["ጼ", "ፄ"],
            ["ፅ", "ጽ"], ["ፆ", "ጾ"], ["ሼ", "ሸ"], ["ሺ", "ሽ"], ["ዲ", "ድ"], ["ጄ", "ጀ"], ["ጂ", "ጅ"], ["ዉ", "ው"], ["ዎ", "ወ"], ["ዴ", "ደ"],
            ["ቼ", "ቸ"], ["ቺ", "ች"], ["ዬ", "የ"], ["ዪ", "ይ"], ["ጬ", "ጨ"], ["ጪ", "ጭ"], ["ኜ", "ኘ"], ["ኚ", "ኝ"], ["ዤ", "ዠ"], ["ዢ", "ዥ"],
        ]
        re_substitutions = [
            [r"ሉ[ዋአ]", "ሏ"], [r"ሙ[ዋአ]", "ሟ"], [r"ቱ[ዋአ]", "ቷ"], [r"ሩ[ዋአ]", "ሯ"], [r"ሱ[ዋአ]", "ሷ"], [r"ሹ[ዋአ]", "ሿ"],
            [r"ቁ[ዋአ]", "ቋ"], [r"ቡ[ዋአ]", "ቧ"], [r"ቹ[ዋአ]", "ቿ"], [r"ሁ[ዋአ]", "ኋ"], [r"ኑ[ዋአ]", "ኗ"], [r"ኙ[ዋአ]", "ኟ"],
            [r"ኩ[ዋአ]", "ኳ"], [r"ዙ[ዋአ]", "ዟ"], [r"ጉ[ዋአ]", "ጓ"], [r"ደ[ዋአ]", "ዷ"], [r"ጡ[ዋአ]", "ጧ"], [r"ጩ[ዋአ]", "ጯ"],
            [r"ጹ[ዋአ]", "ጿ"], [r"ፉ[ዋአ]", "ፏ"], [r"ቊ", "ቁ"], [r"ኵ", "ኩ"], [r"\s+", " "]
        ]

        for old_char, new_char in substitutions:
            norm = norm.replace(old_char, new_char)

        for old_char, new_char in re_substitutions:
            norm = re.sub(old_char, new_char, norm)

        return norm
    
    @staticmethod
    def remove_punctuation(text):
        punctuations = ['!', '@', '#', '\\$', '%', '\\^', '&', '\\*', '\\(', '\\)', '\\[', '\\]', '\\{', '\\}', ';', ':', '\\.', ',', '<', '>', '\\?', '/', '\\|', '~', '=', '\\+', '«', '»', '“', '”', '›', '’', '‘', "'", '\\"', '፡', '።', '፤', '፥', '፦', '፧', '፨', '…','፣', '-']
        text = re.sub(f"[{''.join(punctuations)}]", '', text)
        return AmharicNormalizer.remove_extra_spaces(text)

    @staticmethod
    def remove_non_amharic_chars(text):
        text = re.sub('[a-zA-Z0-9]', '', text)
        return AmharicNormalizer.remove_extra_spaces(text)

    @staticmethod
    def remove_extra_spaces(text):
        text = re.sub('\s+', ' ', text).strip()
        return text

    @staticmethod
    def remove_stop_words(text):
        stopwords = {
        "ህ-ን", "እንደ", "የ", "አል", "ው", "ኡ", "በ", "ተ", "ለ", "ን", "ኦች", "ኧ", "ና", "ከ", "እን", "አንድ", "አይ", "አዎ",
          "አቸው", "ት", "መ", "አ", "አት", "ዎች", "ም", "አስ", "ኡት", "ላ", "ይ", "ማ", "ያ", "አ", "ቶ", "እንዲ", 
         "የሚ", "ኦ", "ይ", "እየ", "ሲ", "ብ", "ወደ", "ሌላ", "ጋር", "ኡ", "እዚህ", "አንድ", "ውስጥ", "እንድ", "እ-ል", "ን-ብ-ር", 
         "በኩል", "ል", "እስከ", "እና", "ድ-ግ-ም", "መካከል", "ኧት", "ሊ", "አይ", "ምክንያት", "ይህ", "ኧች", "ኢት", "ዋና", "አን", 
         "እየ", "ስለ", "ች", "ስ", "ቢ", "ብቻ", "በየ", "ባለ", "ጋራ", "ኋላ", "እነ", "አም", "ሽ", "አዊ", "ዋ", "ያለ", "ግን", "ምን", 
         "አችን", "ወይዘሮ", "ወዲህ", "ማን", "ዘንድ", "የት", "ናቸው", "ላ", "ይሁን", "ወይም", "ታች", "እዚያ", "እጅግ", "እንጅ", "በጣም", 
         "ወዘተ", "ጅ-ም-ር", "አሁን", "ከነ", "ተራ", "ም-ል", "ጎሽ", "አዎ", "እሽ", "ጉዳይ", "ረገድ", "ያህል", "ይልቅ", "ዳር", "እንኳ", 
         "አዎን", "ብ-ዝ", "ጥቂት", "እኔ", "አንተ", "እርስዎ", "እሳቸው", "እሱ", "አንች", "እኛ", "እነሱ", "እናንተ", "ይኸ", "የቱ", "መቼ", 
         "ወይዘሪት", "ትናንት", "ይኽ", "ኤል", "ኦቸ", "ኢዋ", "የለ", "ሰሞን", "ፊት", "ምንጊዜ", "አቸን", "ኧም", "አወ", "ኢያ", "ነገ", 
         "ትላንት", "ኣት", "እንጃ", "ድ-ር-ግ", "መልክ"
        }

        cleaned_text = ' '.join(word for word in text.split() if word not in stopwords)

        return AmharicNormalizer.remove_extra_spaces(cleaned_text)

    
    @staticmethod
    def transliterate(text, lang):
        """
        Transliterate the text from one script to another (Amharic to English or vice versa).
        Args:
            text (str): The text to be transliterated.
            lang (str): Accepts either "en" or "am" to transliterate the given text to either English or Amharic, respectively.

        Returns:
            str: The transliteration text.
        """
        unorm_transliterationPairs = [
            ["chwa", "ቿ"], ["chua", "ቿ"], ["chie", "ቼ"], ["che", "ቸ"], ["chu", "ቹ"], ["chi", "ቺ"], 
            ["cha", "ቻ"], ["cho", "ቾ"], ["hwa", "ኋ"], ["hua", "ኋ"], ["hie", "ሄ"], ["shwa", "ሿ"], 
            ["shua", "ሿ"], ["she", "ሸ"], ["shu", "ሹ"], ["shi", "ሺ"], ["sha", "ሻ"], ["sho", "ሾ"], 
            ["sh", "ሺ"], ["ha", "ሀ"], ["hu", "ሁ"], ["hi", "ሂ"], ["he", "ሄ"], ["ho", "ሆ"], ["lwa", "ሏ"], 
            ["lua", "ሏ"], ["le", "ለ"], ["lu", "ሉ"], ["li", "ሊ"], ["la", "ላ"], ["le", "ሌ"], ["lo", "ሎ"], 
            ["ll", "ል"], ["l", "ል"], ["mwa", "ሟ"], ["mua", "ሟ"], ["mie", "ሜ"], ["me", "መ"], ["mu", "ሙ"], 
            ["mi", "ሚ"], ["ma", "ማ"], ["mo", "ሞ"], ["m", "ም"], ["rwa", "ሯ"], ["rua", "ሯ"], ["rie", "ሬ"], 
            ["re", "ረ"], ["ru", "ሩ"], ["ri", "ሪ"], ["ra", "ራ"], ["ro", "ሮ"], ["rr", "ር"], ["r", "ር"], 
            ["swa", "ሷ"], ["sua", "ሷ"], ["sie", "ሴ"], ["se", "ሰ"], ["su", "ሱ"], ["si", "ሲ"], ["sa", "ሳ"], 
            ["so", "ሶ"], ["qwa", "ቋ"], ["qua", "ቋ"], ["qie", "ቄ"], ["qe", "ቀ"], ["qu", "ቁ"], ["qi", "ቂ"], 
            ["qa", "ቃ"], ["qo", "ቆ"], ["q", "ቅ"], ["bwa", "ቧ"], ["bua", "ቧ"], ["bie", "ቤ"], ["be", "በ"], 
            ["bu", "ቡ"], ["bi", "ቢ"], ["ba", "ባ"], ["bo", "ቦ"], ["b", "ብ"], ["vwa", "ቯ"], ["vua", "ቯ"], 
            ["vie", "ቬ"], ["ve", "ቨ"], ["vu", "ቩ"], ["vi", "ቪ"], ["va", "ቫ"], ["vo", "ቮ"], ["v", "ቭ"],
            ["twa", "ቷ"], ["tua", "ቷ"], ["tie", "ቴ"], ["te", "ተ"], ["tu", "ቱ"], ["ti", "ቲ"], ["ta", "ታ"], 
            ["to", "ቶ"], ["gnwa", "ኟ"], ["gnua", "ኟ"], ["gne", "ኘ"], ["gnu", "ኙ"], ["gni", "ኚ"], 
            ["gna", "ኛ"], ["gno", "ኞ"], ["gn", "ኝ"], ["nwa", "ኗ"], ["nua", "ኗ"], ["nie", "ኔ"], ["ne", "ነ"], 
            ["nu", "ኑ"], ["ni", "ኒ"], ["na", "ና"], ["no", "ኖ"], ["n", "ን"], ["kwa", "ኳ"], ["kua", "ኳ"], 
            ["kie", "ኬ"], ["ke", "ከ"], ["ku", "ኩ"], ["ki", "ኪ"], ["ka", "ካ"], ["ko", "ኮ"], ["k", "ክ"],
            ["wie", "ዌ"], ["we", "ወ"], ["wu", "ው"], ["wi", "ዊ"], ["wa", "ዋ"], ["wo", "ወ"], ["w", "ው"],
            ["zwa", "ዟ"], ["zua", "ዟ"], ["zie", "ዜ"], ["ze", "ዘ"], ["zu", "ዙ"], ["zi", "ዚ"], ["za", "ዛ"], 
            ["zo", "ዞ"], ["zhwa", "ዧ"], ["zhua", "ዧ"], ["zhie", "ዤ"], ["zhe", "ዠ"], ["zhu", "ዡ"], 
            ["zhi", "ዢ"], ["zha", "ዣ"], ["zho", "ዦ"], ["zh", "ዥ"], ["z", "ዝ"], ["ye", "የ"], ["yu", "ዩ"], 
            ["yi", "ዪ"], ["ya", "ያ"], ["yo", "ዮ"], ["y", "ይ"], ["dwa", "ዷ"], ["dua", "ዷ"], ["die", "ዴ"], 
            ["de", "ደ"], ["du", "ዱ"], ["di", "ዲ"], ["da", "ዳ"], ["do", "ዶ"], ["d", "ድ"], ["jwa", "ጇ"], 
            ["jua", "ጇ"], ["je", "ጀ"], ["ju", "ጁ"], ["ji", "ጂ"], ["ja", "ጃ"], ["jo", "ጆ"], ["j", "ጅ"],
            ["gwa", "ጓ"], ["gua", "ጓ"], ["gie", "ጌ"], ["ge", "ገ"], ["gu", "ጉ"], ["gi", "ጊ"], ["ga", "ጋ"], 
            ["go", "ጎ"], ["g", "ግ"], ["chwa", "ጯ"], ["chua", "ጯ"], ["che", "ጨ"], ["chu", "ጩ"], 
            ["chi", "ጪ"], ["cha", "ጫ"], ["cho", "ጮ"], ["ch", "ች"], ["h", "ህ"], ["tswa", "ጿ"], 
            ["tsua", "ጿ"], ["tsie", "ፄ"], ["tse", "ፀ"], ["tsu", "ፁ"], ["tsi", "ፂ"], ["tsa", "ፃ"], 
            ["tso", "ፆ"], ["ts", "ፅ"], ["t", "ት"], ["ss", "ስ"], ["fwa", "ፏ"], ["fua", "ፏ"], ["fie", "ፌ"], 
            ["fe", "ፈ"], ["fu", "ፉ"], ["fi", "ፊ"], ["fa", "ፋ"], ["fo", "ፎ"], ["f", "ፍ"], ["pwa", "ፗ"], 
            ["pua", "ፗ"], ["pie", "ፔ"], ["pe", "ፐ"], ["pu", "ፑ"], ["pi", "ፒ"], ["pa", "ፓ"], ["po", "ፖ"], 
            ["p", "ፕ"], ["ca", "ካ"], ["ci", "ሲ"], ["ce", "ሰ"], ["cu", "ኩ"], ["c ", "ክ"], [" gn ", "ግን"], 
            ["c", "ች"], ["xe", "ዘ"], ["xu", "ዙ"], ["xi", "ዚ"], ["xa", "ዛ"], ["xo", "ዞ"], ["x", "ክስ"], 
            ["xs", "ክስ"], ["s", "ስ"], ["uh", "ኧ"], ["a", "አ"], ["ē","ኤ"], ["u", "ኡ"], ["i", "ኢ"], ["e", "እ"], ["o", "ኦ"],
            [". ", "፡፡"], [";", "፤"], [": ", "፥"], [",", "፣"]
        ]
        transliteration_pairs = [[en_char, AmharicNormalizer.normalize(am_char)] for en_char, am_char in unorm_transliterationPairs]

        if lang == "en":
            for enChar, amChar in transliteration_pairs:
                text = text.replace(amChar, enChar)
        elif lang == "am":
            text = AmharicNormalizer.normalize(text)
            for enChar, amChar in transliteration_pairs:
                text = text.replace(enChar, amChar)
        else:
            raise ValueError("Invalid language! Please choose either 'en' or 'am' for the second argument.")

        return text

    @staticmethod
    def stem(word):
        """
        Reduce the word to its stem form.
        Args:
            word (str): The word to be stemmed.

        Returns:
            str: The stemmed word.
        """
        # Preprocessing and prechecks (assuming these methods exist in this class)
        word = AmharicNormalizer.remove_extra_spaces(word)
        word = AmharicNormalizer.remove_punctuation(word)
        word = AmharicNormalizer.remove_stop_words(word)
        word = AmharicNormalizer.remove_non_amharic_chars(word)
        word = AmharicNormalizer.normalize(word)

        if len(word) < 1:
            return ""
        elif len(word) <= 3:
            return word

        # Setup prefix list
        unorm_prefixes = [
            "ስልኧምኣይ", "ይኧምኣት", "ዕንድኧ", "ይኧትኧ", "ብኧምኣ", "ብኧትኧ", "ዕኧል", "ስልኧ", "ምኧስ", "ዕይኧ", "ዕኧስ", 
            "ዕኧት", "ዕኧን", "ዕኧይ", "ይኣል", "ስኣት", "ስኣን", "ስኣይ", "ስ ኣል", "ይኣስ", "ይኧ", "ልኧ", "ክኧ", "እን", 
            "ዕን", "ዐል", "ይ", "ት", "አ", "እ"
        ]
        prefixes = [AmharicNormalizer.normalize(prefix) for prefix in unorm_prefixes]

        # Setup suffix list
        unorm_suffixes = [
            "ኢዕኧልኧሽ", "ኣውኢው", "አዊው", "ኣችኧውኣል", "ኧችኣት", "ኧቻት", "ኧችኣችህኡ", "ኧቻቹ", "ኧችኣችኧው","ኧቻቸው", "ኣልኧህኡ", 
            "አልሁ","ኣውኦች", "ኣልኧህ","አለህ", "ኣልኧሽ","አልሽ","ኣልችህኡ", "ኣልችሁ", "ኣልኣልኧች","ኣላለች", "ብኣችኧውስ", "ባቸውስ", "ብኣችኧው","ባቸው", "ኣችኧውን", "ኣቸውን", "ኣልኧች","አለች", "ኣልኧን", "አለን", "ኣልኧው", "አለው",
            "ኣልኣችህኡ","አላቹ","አላችሁ", "ኣችህኡን","አችሁን","አቹን", "ኣችህኡ", "ኣችሁ","ኣቹ", "ኣችህኡት", "ኣችሁት","ውኦችንንኣ","ዎችና", "ውኦችን","ዋችን", "ኣችኧው","ኣቸው", "ውኦችኡን","ዎችን", "ውኦችኡ", "ዎቹ", "ኧውንኣ","ኧውና", 
            "ኦችኡን", "ኦቹን", "ኦውኦች", "አዎች", "ኧኝኣንኧትም", "ኧኛነትም", "ኧኝኣንኣ","ኧኛና", "ኧኝኣንኧት", "ኧኛነት", "ኧኝኣን","ኘን", "ኧኝኣውም", "ኛውም", "ኧኝኣው", "ኛው", "ኝኣውኣ","ኛዋ", "ብኧትን","በትን", 
            "ኣችህኡም", "ኦውኣ","አዋ", "ኧችው", "ኧችኡ","ኧቹ", "ኤችኡ", "ንኧው","ነው", "ንኧት","ነት", "ኣልኡ", "አሉ", "ኣችን", "ክኡም","ኩም", "ክኡት", "ኩት","ክኧው", "ከው",
            "ኧችን", "ኧችም", "ኧችህ", "ኧችሽ", "ኧችን", "ኧችው", "ይኡሽን", "ይኡሽ","ዩሽ", "ኧውኢ","ኧዊ", "ኦችንንኣ","ኦችና", "ኣውኢ","አዊ", "ብኧት", "በት",
            "ኦች", "ኦችኡ", "ኦቹ", "ውኦን", "ኧኝኣ", "ኝኣውን", "ኝኣው", "ኦችን", "ኣል", "ኧም", "ሽው", "ክም", "ኧው", "ትም", "ውኦ", "ዎ", 
            "ውም", "ውን", "ንም", "ሽን", "ኣች", "ኡት", "ኢት", "ክኡ","ኩ", "ኤ", "ህ", "ሽ", "ኡ", "ሽ", "ክ", "ኧ", "ኧች", 
            "ኡን", "ን", "ም", "ንኣ","ና", "ው"
        ]
        suffixes = [AmharicNormalizer.normalize(suffix) for suffix in unorm_suffixes]

        # Setup affix substitutions list
        unorm_affix_substitutions = [["ዕንድኣ", "ዕኣ"], ["ጭኣል", "ጥኣል"], ["ዕኧልኣ", "ዕኣ"]]
        affix_substitutions = [[AmharicNormalizer.normalize(x[0]), AmharicNormalizer.normalize(x[1])] for x in unorm_affix_substitutions]


        word_CV_form = AmharicNormalizer.transliterate(word, "en")

        if len(word_CV_form) > 2:
            for substitution in affix_substitutions:
                word_CV_form = word_CV_form.replace(
                    AmharicNormalizer.transliterate(substitution[0], "en"),
                    AmharicNormalizer.transliterate(substitution[1], "en")
                )

            if word_CV_form[-1] == AmharicNormalizer.transliterate("ኝ", "en"):
                word_CV_form = word_CV_form.replace(
                    AmharicNormalizer.transliterate("እኧስ", "en"),
                    AmharicNormalizer.transliterate("ስ", "en")
                )
                word_CV_form = word_CV_form[:-1]

            if word_CV_form[0] == AmharicNormalizer.transliterate("ዕ", "en") and word_CV_form[2] == AmharicNormalizer.transliterate("ኧ", "en"):
                word_CV_form = word_CV_form[1:]

        if len(word_CV_form) > 3:
            for suffix in suffixes:
                transliterated = AmharicNormalizer.transliterate(suffix, "en")
                if word_CV_form.endswith(transliterated):
                    word_CV_form = word_CV_form[:-len(transliterated)]

        if len(word_CV_form) > 3:
            for prefix in prefixes:
                transliterated = AmharicNormalizer.transliterate(prefix, "en")
                if word_CV_form.startswith(transliterated):
                    word_CV_form = word_CV_form[len(transliterated):]

        word_stem = re.sub('[aeiou]', '', word_CV_form)
        return AmharicNormalizer.transliterate(word_stem, "am")