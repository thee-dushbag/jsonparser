#include <string_view>
#include <iostream>

#pragma once

namespace Json {

  namespace __impl {
    enum class _kind {
#define F(TK) TK,
# include "tokens.def"
#undef F
    };

    struct _location {
      unsigned int
        line, column;
    };
  }

  struct Token {
    using Kind = __impl::_kind;
    using Location = __impl::_location;

    Kind kind;
    Location location;
    std::string_view content;
    const char* error;
  };

  std::ostream& operator<<(std::ostream& out, Token const& tk);
  const char* to_string(Token::Kind);

  struct Lexer {
    void feed(std::string_view source);
    Lexer(std::string_view source);
    void reset();
    Token get();
    Lexer();

  private:
    Token make_etoken(const char* error);
    Token consume_token(Token::Kind kind);
    Token make_ctoken(Token::Kind kind);
    Token make_token(Token::Kind kind);
    std::string_view lexeme();
    bool match(char expected);
    char peek(int offset = 0);
    std::size_t length();
    Token identifier();
    void advance();
    void consume();
    Token string();
    Token number();
    bool empty();
    bool space();

    unsigned int line, column;
    const char* start, * head;
    std::string_view src;
    Token::Location location;
  };
}
