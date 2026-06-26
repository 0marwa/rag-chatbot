import argparse
import sys

from src.rag import ask, ingest


def cmd_ingest(args: argparse.Namespace) -> None:
    print(f"ingesting docs from {args.data_dir}/ ...")
    n = ingest(args.data_dir)
    if n:
        print(f"done. {n} chunks stored.")


def cmd_chat(args: argparse.Namespace) -> None:
    print("chat started. type 'quit' or ctrl+c to exit.")
    if args.debug:
        print("debug mode on: retrieved chunks will be shown.\n")
    try:
        while True:
            question = input("you: ").strip()
            if not question:
                continue
            if question.lower() in ("quit", "exit"):
                break
            result = ask(question, debug=args.debug)
            print(f"\nbot: {result['answer']}")
            if result["sources"]:
                print(f"sources: {', '.join(result['sources'])}")
            print()
    except KeyboardInterrupt:
        print("\nbye.")
        sys.exit(0)


def main() -> None:
    parser = argparse.ArgumentParser(description="rag chatbot cli")
    sub = parser.add_subparsers(dest="command")

    ingest_parser = sub.add_parser("ingest", help="load docs into the vector store")
    ingest_parser.add_argument("--data-dir", default="data", help="folder with your docs (default: data/)")

    chat_parser = sub.add_parser("chat", help="ask questions about your docs")
    chat_parser.add_argument("--debug", action="store_true", help="show retrieved chunks for each answer")

    args = parser.parse_args()

    if args.command == "ingest":
        cmd_ingest(args)
    elif args.command == "chat":
        cmd_chat(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
