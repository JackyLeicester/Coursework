def i_am_lazy(errors: list, passes: list)->str:
    output: str = ""
    for index, file in enumerate(errors, 1):
        output += f"""
    def test{index}(self):
        expect_exception(self, "{file}")
                """
    
    for index, file in enumerate(passes, len(errors)):
        output += f"""
    def test{index}(self):
        output: str = run_test("{file}")
        self.assertEqual(output, "")
                """
    return output

if __name__ == "__main__":
    errors: list = [
        "AAA({",
        "AAA(}",
        "AAA(),",
        "AAA()AAA",
    ]
    passes: list = [
        "AAA();"
    ]
    print(i_am_lazy(errors, passes))