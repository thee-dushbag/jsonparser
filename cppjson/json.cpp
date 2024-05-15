#ifndef __JSON_SNN_IMPL_
#define __JSON_SNN_IMPL_

#include "json.hpp"
#include <utility>

namespace Json {
  const char* to_string(Token::Kind kind) {
    using enum Token::Kind;
    switch ( kind ) {
#define Str(V) #V
#define F(K) case K: return Str(Kind_ ## K);
#include "tokens.def"
#undef F
#undef V
    }
    std::unreachable();
  }

  std::ostream& operator<<(std::ostream& out, Token const& tk) {
    out << "Token(" << to_string(tk.kind) << ", '" << tk.content
      << "', " << tk.location.line << ":" << tk.location.column;
    if ( tk.error != nullptr ) out << ", cause='" << tk.error << "'";
    return out << ')';
  }

  Token Lexer::make_etoken(const char* error) {
    return { Token::Kind::Error, location, lexeme(), error };
  }

  Token Lexer::make_token(Token::Kind kind) {
    return { kind, location, lexeme(), nullptr };
  }

  Lexer::Lexer() { reset(); }
  bool Lexer::empty() { return head >= src.cend(); }
  Lexer::Lexer(std::string_view source) { reset(); feed(source); }
  std::string_view Lexer::lexeme() { return { start, length() }; }
  char Lexer::peek(int offset) { return *(head + offset); }
  std::size_t Lexer::length() { return head - start; }

  void Lexer::feed(std::string_view source) {
    head = start = (src = source).begin();
  }

  void Lexer::advance() {
    if ( *++head == '\n' ) {
      column = 0;
      line++;
    } else column++;
  }

  bool Lexer::match(char expected) {
    return (peek() == expected) ?
      (advance(), true) : false;
  }

  void Lexer::consume() {
    location = { line, column };
    start = head;
  }

  Token Lexer::consume_token(Token::Kind kind) {
    Token tk = make_token(kind);
    return (consume(), tk);
  }

  bool Lexer::space() {
    while ( not empty() )
      if ( not(match('\t') or match('\n') or match(' ')) )
        break;
    // Discard all gathered spaces and return if it is now empty
    return (consume(), empty());
  }

  Token Lexer::make_ctoken(Token::Kind kind) {
    // Consume a character then make and return a token
    return (advance(), consume_token(kind));
  }

  Token Lexer::string() {
    advance(); // Consume Openning quote
    while ( not empty() and peek() != '"' )
      if ( (advance(), peek(-1) == '\n') )
        return make_etoken(
          "Multiline strings are not supported. "
          "String Unterminated."
        );
    return empty() ?
      make_etoken("Unterminated string.") :
      // Consume the Closing Quote and create a string token
      make_ctoken(Token::Kind::String);
  }

  Token Lexer::number() {
    while ( not empty() and std::isdigit(peek()) ) advance();
    return make_token(Token::Kind::Number);
  }

  Token Lexer::identifier() {
    while ( not empty() and (std::isalnum(peek()) or peek() == '_') ) advance();
    return lexeme() == "true" ? make_token(Token::Kind::True) :
      lexeme() == "false" ? make_token(Token::Kind::False) :
      lexeme() == "null" ? make_token(Token::Kind::Null) :
      make_etoken("Unexpected name token, expected true, null or false.");
  }

  void Lexer::reset() {
    src = { };
    head = start = src.begin();
    line = 1, column = 0;
  }

  Token Lexer::get() {
    using enum Token::Kind;
    while ( not space() ) {
      switch ( peek() ) {
      case '{': return make_ctoken(OpenBrace);
      case '}': return make_ctoken(CloseBrace);
      case '[': return make_ctoken(OpenBracket);
      case ']': return make_ctoken(CloseBracket);
      case ':': return make_ctoken(Colon);
      case ',': return make_ctoken(Comma);
      case '"': return string();
      default:
        if ( std::isdigit(peek()) ) return number();
        if ( std::isalnum(peek()) ) return identifier();
        return make_etoken("Unexpected character.");
      }
    }
    return make_token(Eot);
  }
}

#endif //__JSON_SNN_IMPL_
