translator = function()
    local this = {}

    this.__private = {
        num_symbols_used_to_encode = 3,
        encoding_alphabet = {},
        message_alphabet = {},
    }

end

Person = {}
function Person:new(lang_uniq_symbols)

    local public = {}
        function public:encode(message)
            local encoded_data = {}
            private:array_concat(encoded_data, private.head)
            private:array_concat(encoded_data, private.encoding_alphabet)

            for _, val in ipairs(message) do
                local encoded_char = private.encoding_table[val]
                private:array_concat(encoded_data, {encoded_char})
            end

            private:array_concat(encoded_data, private.tail)
            local encoded_string =
        end

        function public:Decode(message)
            return "dummy"
        end

    local private = {}
        numSymbolsUsedToEncode = 3,
        encoding_alphabet = lang_uniq_symbols,
        messageAlphabet = private:private:__setup_message_alphabet(),
        head = private:__get_prefix(),
        tail = private:__get_postfix(),
        encoding_table = private:__setup_encoding_table(),
        decodingTable = private.__setup_decoding_table(),

        function private:__setup_message_alphabet()
            ascii_lowercase = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'}
            ascii_uppercase = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'}
            cyrillic_lowercase = {'е', 'ц', 'ь', 'ю', 'л', 'т', 'й', 'ж', 'д', 'б', 'п', 'ф', 'ч', 'г', 'ъ', 'у', 'к', 'р', 'о', 'а', 'з', 'х', 'в', 'с', 'я', 'м', 'э', 'и', 'н', 'ы', 'щ', 'ё', 'ш', 'і', 'є', 'ї'}
            cyrillic_uppercase = {'Е', 'Ц', 'Ь', 'Ю', 'Л', 'Т', 'Й', 'Ж', 'Д', 'Б', 'П', 'Ф', 'Ч', 'Г', 'Ъ', 'У', 'К', 'Р', 'О', 'А', 'З', 'Х', 'В', 'С', 'Я', 'М', 'Э', 'И', 'Н', 'Ы', 'Щ', 'Ё', 'Ш', 'І', 'Є', 'Ї'}
            digits = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
            punctuation = {'!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~'}
            special_chars = {' '}

            local alphabet = private:array_concat(
                ascii_lowercase,
                ascii_uppercase,
                cyrillic_lowercase,
                cyrillic_uppercase,
                digits,
                punctuation,
                special_chars
            )
            return alphabet
        end

        function private:__get_prefix()
            local symbol_index = -1
            local encoding_value = private.encoding_alphabet[symbol_index]
            local prefix = string.rep(encoding_value, private.numSymbolsUsedToEncode - 1) .. private.encoding_alphabet[1]
            return prefix
        end

        function private:__get_postfix()
            local symbol_index = -1
            local encoding_value = private.encoding_alphabet[symbol_index]
            local prefix = string.rep(encoding_value, private.numSymbolsUsedToEncode - 1) .. private.encoding_alphabet[2]
            return prefix
        end

        function private:array_concat(...)
            local t = {}
            for n = 1,select("#",...) do
                local arg = select(n,...)
                if type(arg)=="table" then
                    for _,v in ipairs(arg) do
                        t[#t+1] = v
                    end
                else
                    t[#t+1] = arg
                end
            end
            return t
        end

        function private:__setup_encoding_table()
            local encoding_table

            for i, a in ipairs(private.encoding_alphabet) do
                for _, b in ipairs(private.encoding_alphabet) do
                    for _, a in ipairs(private.encoding_alphabet) do
                        encoding_table.insert(tostring(a)..tostring(b)..tostring(c))
                    end
                end
            end
            return encoding_table
        end

        function private:__setup_decoding_table()
            local decodingTable

            for key, val in pairs(private.encoding_table) do
                decodingTable[val] = key
            end
            return decodingTable
        end

    setmetatable(public,self)
    self.__index = self; return public
end
