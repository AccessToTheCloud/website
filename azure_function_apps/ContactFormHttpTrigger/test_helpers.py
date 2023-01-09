import unittest
import helpers


class TestHelpers(unittest.TestCase):

    def test_validate_email(self):
        test_cases = [
            # Valid
            ("simple@example.com", "simple@example.com"),
            ("very.common@example.com", "very.common@example.com"),
            ("disposable.style.email.with+symbol@example.com",
             "disposable.style.email.with+symbol@example.com"),
            ("other.email-with-hyphen@example.com",
             "other.email-with-hyphen@example.com"),
            ("fully-qualified-domain@example.com",
             "fully-qualified-domain@example.com"),
            ("user.name+tag+sorting@example.com",
             "user.name+tag+sorting@example.com"),
            ("x@example.com", "x@example.com"),
            ("example-indeed@strange-example.com",
             "example-indeed@strange-example.com"),
            ("test/test@test.com", "test/test@test.com"),
            ("admin@mailserver1", "admin@mailserver1"),
            ("example@s.example", "example@s.example"),
            ("mailhost!username@example.org", "mailhost!username@example.org"),
            ("user%example.com@example.org", "user%example.com@example.org"),
            ("user-@example.org", "user-@example.org"),
            ("postmaster@[123.123.123.123]", "postmaster@[123.123.123.123]"),
            ("postmaster@[IPv6:2001:0db8:85a3:0000:0000:8a2e:0370:7334]",
             "postmaster@[IPv6:2001:0db8:85a3:0000:0000:8a2e:0370:7334]"),
            # Invalid
            ('Abc.example.com', None),
            ('A@b@c@example.com', None),
            ('just"not"right@example.com', None),
            ('this is"not\allowed@example.com', None),
            ('QA[icon]CHOCOLATE[icon]@test.com', None),
        ]

        for (email, result) in test_cases:
            self.assertEqual(helpers.validate_email(email), result)


if __name__ == '__main__':
    unittest.main()
