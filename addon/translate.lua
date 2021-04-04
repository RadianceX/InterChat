SlashCmdList["TS"] = function(msg, editBox) parse_input(msg, editBox) end
translator_obj = nil



function Translator_Init()
	local this = CreateFrame("Frame", "Translator", UIParent);
	this:SetScript("OnEvent", Translator_OnEvent);
	this:RegisterEvent("PLAYER_LOGIN");
    translator_obj = Translator()
end

function colorized_message(msg)
	DEFAULT_CHAT_FRAME:AddMessage("|cFFFFAA11"..msg.."|r")
end

function parse_input(msg, editBox)
	if (not msg or msg == "") then
		colorized_message("    Cross-language communication add-on. Use at your own risk!")
		colorized_message("    The maximum message length is 42 characters. Usage...")
		colorized_message("        /ts (the message you want to translate)")
	else
		if (string.len(msg) < 40) then
			local encoder = languages[editBox.language]
			if (encoder ~= nil) then
				SendChatMessage(Translator_Encode(msg, encoder), "SAY", editBox.language)
			else
				colorized_message(editBox.language.." language is not supported.")
			end
		else
			colorized_message("Message too long to encode. Type /trans for usage.")
		end
	end
end