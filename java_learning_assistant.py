from gemini_assistant import GeminiJavaAssistant

def main():
    assistant = GeminiJavaAssistant()
    print("✨" + "=" * 50)
    print("🎓 JAVA LEARNING ASSISTANT")
    print("=" * 52)
    print("🚀 AI-Powered Java Education Platform")
    print("🤖 Powered by Google Gemini")
    print("✨" + "=" * 50)
    print(f"\n📊 Status: {assistant.get_status()}")
    print("\n📝 Ask me anything about Java programming!")
    print("💡 Examples: 'explain inheritance', 'show me a loop example'")
    print("🚪 Type 'quit' to exit\n")
    
    while True:
        try:
            user_input = input("💬 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye', 'q']:
                print("\n🎉 Happy coding! Keep practicing Java! 🚀")
                break
            
            if not user_input:
                continue
            
            response = assistant.chat(user_input)
            print(f"🤖 Assistant: {response}\n")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Happy coding! 🚀")
            break
        except Exception as e:
            print(f"\n⚠️ Error: {e}")
            print("Please try again.\n")

if __name__ == "__main__":
    main()