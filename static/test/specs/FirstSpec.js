define(['jquery', 'underscore'], function($, _) {
    describe("Another suite", function () {
        it("contains spec with a new", function () {
            expect(true).toBe(true);
            expect(_.first([1,2,3])).toBe(1);
        });
    });
});
